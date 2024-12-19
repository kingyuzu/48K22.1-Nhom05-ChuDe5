from .models import Ticket
from datetime import datetime, timedelta
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError

from .forms.campaign import CampaignForm
from .models import Product, Ticket, Campaign, MailTrack, Contact, User, Order, OrderDetail
from .serializers.ticket import (
    TicketSerializer,
    CampaignSerializer,
    MailTrackSerializer,
    ContactSerializer,
    UserSerializer,
    OrderSerializer,
)
import base64
import traceback
from django.db.models import Q
import csv


class TicketAPIView(APIView):
    def get(self, request, ticket_id=None):
        """
        Fetch a single ticket by ID or list all tickets.
        """
        if ticket_id:
            try:
                ticket = Ticket.objects.get(ticket_id=ticket_id)
                serializer = TicketSerializer(ticket)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Ticket.DoesNotExist:
                return Response(
                    {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new ticket.
        """
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, ticket_id=None):
        """
        Update an existing ticket by ID.
        """
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticket_id=None):
        """
        Delete a ticket by ID.
        """
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.delete()
            return Response(
                {"message": "Ticket deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )


def ticket_view(request):
    query_string_name = request.GET.get("name") or ""
    if query_string_name:
        # Queries all products from the database
        new_tickets = Ticket.objects.filter(Q(status=Ticket.TicketStatus.NEW) & (
            Q(title__icontains=query_string_name) | Q(description__icontains=query_string_name)))
        waiting_on_contact_tickets = Ticket.objects.filter(
            Q(status=Ticket.TicketStatus.WAITING_ON_CONTACT) & (Q(title__icontains=query_string_name) | Q(description__icontains=query_string_name)))
        in_progress_tickets = Ticket.objects.filter(
            Q(status=Ticket.TicketStatus.IN_PROGRESS) & (Q(title__icontains=query_string_name) | Q(description__icontains=query_string_name)))
        solved_tickets = Ticket.objects.filter(
            Q(status=Ticket.TicketStatus.SOLVED) & (Q(title__icontains=query_string_name) | Q(description__icontains=query_string_name)))
        closed_tickets = Ticket.objects.filter(
            Q(status=Ticket.TicketStatus.CLOSED) & (Q(title__icontains=query_string_name) | Q(description__icontains=query_string_name)))

    else:
        # Queries all products from the database
        new_tickets = Ticket.objects.filter(status=Ticket.TicketStatus.NEW)
        waiting_on_contact_tickets = Ticket.objects.filter(
            status=Ticket.TicketStatus.WAITING_ON_CONTACT
        )
        in_progress_tickets = Ticket.objects.filter(
            status=Ticket.TicketStatus.IN_PROGRESS)
        solved_tickets = Ticket.objects.filter(
            status=Ticket.TicketStatus.SOLVED)
        closed_tickets = Ticket.objects.filter(
            status=Ticket.TicketStatus.CLOSED)

    # Get all order
    orders = Order.objects.all()
    return render(
        request,
        "ticket/index.html",
        {
            "new_tickets": new_tickets,
            "waiting_on_contact_tickets": waiting_on_contact_tickets,
            "in_progress_tickets": in_progress_tickets,
            "solved_tickets": solved_tickets,
            "closed_tickets": closed_tickets,
            "orders": orders,
            "query_string_name": query_string_name,
        },
    )


def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(
        request,
        "ticket/detail.html",
        {
            "ticket": ticket,
        },
    )


class ContactAPIView(APIView):

    # GET
    # POST
    # PUT
    # DELETE

    def get(self, request, contact_id=None):
        """
        Fetch a single Contact by ID or list all Contacts.
        """
        if contact_id:
            try:
                item = Contact.objects.get(contact_id=contact_id)
                serializer = ContactSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Contact.DoesNotExist:
                return Response(
                    {"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            items = Contact.objects.all()
            serializer = ContactSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new Contact along with a related User.
        """
        # Validate Contact data
        serializer = ContactSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract User-related data
        user_data = {
            "username": request.data.get("email"),
            "email": request.data.get("email"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone_number": request.data.get("phone_number"),
            "address": request.data.get("address"),
            "user_type": User.UserType.CUSTOMER,
            "date_join": datetime.now().date(),
            "password": request.data.get("password", "defaultpassword"),
        }
        if User.objects.filter(username=user_data["username"]).exists():
            return Response(
                {"error": "Username (email) already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create User
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data["phone_number"],
                address=user_data["address"],
                user_type=user_data["user_type"],
                date_join=user_data["date_join"],
                password=user_data["password"],
            )
            user.save()
            # Get user have just created
            new_user = User.objects.get(username=user.username)
            owner_user = User.objects.get(
                username=request.data.get("owner_username"))

            # # Save Contact and link to the created User
            contact = serializer.save(user=new_user, owner=owner_user)
            return Response(
                ContactSerializer(contact).data, status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print traceback
            print(traceback.format_exc())
            return Response(
                {"error": "An error occurred while creating the contact and user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, contact_id=None):
        try:
            contact = Contact.objects.get(contact_id=contact_id)
        except Contact.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # `partial=True` allows partial updates
        serializer = ContactSerializer(
            contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        # Update User data (related to the contact)
        user = contact.user  # Get the related User object
        user_serializer = UserSerializer(
            user, data=request.data, partial=True
        )  # Update the User
        if user_serializer.is_valid():
            user_serializer.save()

            # Return both the updated contact and user data
            return Response(
                {"contact": serializer.data, "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, contact_id=None):
        """
        Delete a item by ID.
        """
        try:
            item = Contact.objects.get(contact_id=contact_id)
            item.delete()
            return Response(
                {"message": "Contact deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND
            )


def contact_view(request):
    # truy van csdl, table contact, luu vao bien va hien thi tren trang contact.html
    contacts = Contact.objects.all()

    # Filter by created date if provided in query string
    # Expecting a format like '2024-12-01'
    created_date = request.GET.get("created_date")
    print("created_date", created_date)
    if created_date:
        try:
            created_date_obj = datetime.strptime(created_date, "%Y-%m-%d")
            print("created_date_obj", created_date_obj)
            contacts = contacts.filter(created_date__date=created_date_obj)
        except ValueError:
            print("33")
            pass  # Ignore invalid date format

    # Filter by lifecycle stage if provided in query string
    lifecycle_stage = request.GET.get("lifecycle_stage")
    if lifecycle_stage:
        contacts = contacts.filter(lifecycle_stage=lifecycle_stage)

    client_this_week = Contact.objects.filter(
        created_date__gte=datetime.now() - timedelta(days=7)
    ).order_by("-created_date")[
        :6
    ]  # Top 6 contacts created this week

    return render(
        request,
        "contact/index.html",
        {"client_this_week": client_this_week, "contacts": contacts},
    )

def export_contacts_csv(request):
    # Tạo HTTP response với content type là text/csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    # Tạo writer cho file CSV
    writer = csv.writer(response)

    # Thêm header vào file CSV
    writer.writerow([
        'Contact ID',
        'Username',
        'Address',
        'Lifecycle Stage',
        'Created Date',
        'Owner Username'
    ])

    # Lấy tất cả các `Contact` từ database
    contacts = Contact.objects.all()

    # Ghi từng dòng dữ liệu của `Contact` vào file CSV
    for contact in contacts:
        writer.writerow([
            contact.contact_id,
            contact.user.username,
            contact.address,
            contact.lifecycle_stage,
            contact.created_date.strftime('%Y-%m-%d %H:%M:%S') if contact.created_date else '',
            contact.owner.username if contact.owner else ''
        ])

    return response

def contact_detail_view(request, contact_id):
    contact = get_object_or_404(Contact, contact_id=contact_id)

    # Lấy thông tin người dùng
    user = User.objects.get(id=contact.user.id)

    # Lấy lịch sử đơn hàng
    orders = Order.objects.filter(contact_name__user=user).values(
        "order_id", "status", "total_price", "created_date"
    )

    # Lấy danh sách ticket
    tickets = Ticket.objects.filter(user=user).values(
        "ticket_id",
        "subject",
        "title",
        "status",
        "priority",
        "created_date",
        "description",
    )

    deta = {
        "orders": list(orders),
        "tickets": list(tickets),
    }
    print("deta", deta.get("orders"))
    print("deta", deta.get("tickets"))

    return render(
        request,
        "contact/detail.html",
        {
            "contact": contact,
            "orders": list(orders),
            "tickets": list(tickets),
        },
    )


def product_view(request):

    # Lấy từ DB ra
    # ...
    product_list = Product.objects.all()
    print("san pham cua toi", product_list)

    return render(
        request,
        "product/index.html",
        {
            "products": product_list,
        }
    )


def product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(
        request,
        "product/detail.html",
        {
            "product": product
        },
    )


class OrderAPIView(APIView):
    def get(self, request, order_id=None):
        """
        Fetch a single Order by ID
        """
        if order_id:
            try:
                item = Order.objects.get(id=order_id)
                serializer = OrderSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Contact.DoesNotExist:
                return Response(
                    {"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND
            )


def order_view(request):
    orders_new = []
    orders_confirmed = []
    orders_in_progress = []
    orders_delivered = []
    orders_returned = []
    price_from = float(request.GET.get("price-from") or "0")
    price_to = float(request.GET.get("price-to") or "0")
    if price_from >= 0 and price_to >= 0 and price_from < price_to:
        orders_new = Order.objects.filter(
            status=Order.OrderStatus.NEW, total_price__gte=price_from, total_price__lte=price_to)
        orders_confirmed = Order.objects.filter(
            status=Order.OrderStatus.CONFIRMED, total_price__gte=price_from, total_price__lte=price_to)
        orders_in_progress = Order.objects.filter(
            status=Order.OrderStatus.IN_PROGRESS, total_price__gte=price_from, total_price__lte=price_to)
        orders_delivered = Order.objects.filter(
            status=Order.OrderStatus.DELIVERED, total_price__gte=price_from, total_price__lte=price_to)
        orders_returned = Order.objects.filter(
            status=Order.OrderStatus.RETURNED, total_price__gte=price_from, total_price__lte=price_to)
    else:
        # Lấy danh sách đơn hàng theo trạng thái
        orders_new = Order.objects.filter(status=Order.OrderStatus.NEW)
        orders_confirmed = Order.objects.filter(
            status=Order.OrderStatus.CONFIRMED)
        orders_in_progress = Order.objects.filter(
            status=Order.OrderStatus.IN_PROGRESS)
        orders_delivered = Order.objects.filter(
            status=Order.OrderStatus.DELIVERED)
        orders_returned = Order.objects.filter(
            status=Order.OrderStatus.RETURNED)
    # Render template và truyền danh sách đơn hàng vào context

     # Lấy đơn hàng mới nhất của ngày hôm nay
    orders_today = Order.objects.filter(
        created_date__date=datetime.now().date())
    print("orders_today", orders_today)
    return render(
        request,
        "order/index.html",
        {
            "orders_new": orders_new,
            "orders_confirmed": orders_confirmed,
            "orders_in_progress": orders_in_progress,
            "orders_delivered": orders_delivered,
            "orders_returned": orders_returned,
            "orders_today": orders_today,
            "price_from": price_from,
            "price_to": price_to,
        },
    )


def order_detail_view(request, order_id):
    # Fetch the order and related details
    order = get_object_or_404(Order, order_id=order_id)
    order.total_price = f"{order.total_price:,.0f}"
    order_details = OrderDetail.objects.filter(order=order)

    # Calculate subtotals for each item (if needed in template)
    total_products = 0
    for detail in order_details:
        print("detail.product.quantity", detail.product.quantity)
        total_products += detail.quantity
        detail.subtotal = f"{detail.quantity * detail.product.unit_price:,.0f}"
        detail.product.unit_price = f"{detail.product.unit_price:,.0f}"

    current_status_num = ["NEW", "CONFIRMED", "IN_PROGRESS",
                          "DELIVERED", "RETURNED"].index(order.status)
    return render(
        request,
        "order/detail.html",
        {
            "order": order,
            "total_products": total_products,
            "order_details": order_details,
            "current_status_num": current_status_num,
        },
    )


class CampaignAPIView(APIView):
    def get(self, request, campaign_id=None):
        """
        Fetch a single campaign by ID or list all campaigns.
        """
        if campaign_id:
            try:
                item = Campaign.objects.get(campaign_id=campaign_id)
                serializer = CampaignSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Campaign.DoesNotExist:
                return Response(
                    {"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            items = Campaign.objects.all()
            serializer = CampaignSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new campaign.
        """
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(staff=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, campaign_id=None):
        try:
            item = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # `partial=True` allows partial updates
        serializer = CampaignSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, campaign_id=None):
        """
        Delete a item by ID.
        """
        try:
            item = Campaign.objects.get(campaign_id=campaign_id)
            item.delete()
            return Response(
                {"message": "Campaign deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND
            )


def campaign_view(request):
    # Queries all campaign from the database
    campaigns = Campaign.objects.all()

    campaign_list = []
    for campaign in campaigns:
        # Tổng số MailTrack trong chiến dịch
        total_tracks = MailTrack.objects.filter(campaign=campaign).count()

        # Số MailTrack được mở (is_open=True)
        opened_tracks = MailTrack.objects.filter(
            campaign=campaign, is_open=True
        ).count()

        # Số MailTrack được click (is_click=True)
        clicked_tracks = MailTrack.objects.filter(
            campaign=campaign, is_click=True
        ).count()

        # Tính toán open_rate và clicked_rate
        open_rate = (opened_tracks / total_tracks *
                     100) if total_tracks > 0 else 0
        clicked_rate = (clicked_tracks / total_tracks *
                        100) if total_tracks > 0 else 0

        # Thêm thông tin vào campaign
        campaign_list.append(
            {
                "campaign_data": campaign,
                "open_rate": round(open_rate, 2),
                "crt": round(clicked_rate, 2),
            }
        )

    return render(
        request,
        "campaign/index.html",
        {
            "campaign_list": campaign_list,
            "status_choices": Campaign.StatusChoices.choices,
        },
    )


def campaign_detail_view(request, campaign_id):
    # Lấy chiến dịch hoặc trả về 404 nếu không tồn tại
    campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
    mail_tracks = MailTrack.objects.filter(campaign=campaign)

    # Tính tổng số email đã gửi
    total_sent = mail_tracks.filter(is_send=True).count()

    # Tính số email đã mở
    total_opened = mail_tracks.filter(is_open=True).count()

    # Tính số email có link được nhấp
    total_clicked = mail_tracks.filter(is_click=True).count()

    # Tính toán open_rate và crt
    open_rate = (total_opened / total_sent * 100) if total_sent > 0 else 0
    crt = (total_clicked / total_sent * 100) if total_sent > 0 else 0

    campaign_data = {
        "campaign": campaign,  # Đối tượng Campaign
        "open_rate": round(open_rate, 2),
        "crt": round(crt, 2),
    }

    # Trả về template cùng với dữ liệu của chiến dịch

    # Lấy danh sách các contact_id đã có trong MailTrack với campaign_id
    added_contacts = MailTrack.objects.filter(campaign_id=campaign_id).values_list(
        "contact_id"
    )

    # Lấy danh sách các Contact chưa có trong MailTrack với campaign_id
    untracked_contacts = Contact.objects.exclude(id__in=added_contacts)

    return render(
        request,
        "campaign/campaign_detail.html",
        {
            "campaign_data": campaign_data,
            "mail_tracks": mail_tracks,
            "untracked_contacts": untracked_contacts,
        },
    )


def update_campaign_email(request, campaign_id):
    campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
    print("udpate for campaign", campaign)
    if request.method == "POST":
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            print("form", form)
            form.save()
            return redirect("admin-campaign-detail", campaign_id=campaign.campaign_id)
        else:
            print("form invalid")
    else:
        form = CampaignForm(instance=campaign)

    return render(request, "update_campaign.html", {"form": form, "campaign": campaign})


class AddEmailsToCampaignAPIView(APIView):
    def post(self, request, campaign_id):
        # Lấy chiến dịch từ database
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        # Lấy danh sách email từ request payload
        email_list = request.data.get("emails")
        for email in email_list:
            contact = Contact.objects.get(user__email=email)
            mail_track = MailTrack(
                contact=contact,  # ForeignKey to Contact
                campaign=campaign,  # ForeignKey to Campaign
            )
            mail_track.save()

        return JsonResponse({"status": "Saved"})


class SendCampaignEmailAPIView(APIView):
    def post(self, request, campaign_id):
        """
        Gửi email HTML đến danh sách người nhận trong request payload.
        """
        # Lấy chiến dịch từ database
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        subject = campaign.mail_subject
        message = (
            f"Chào bạn, đừng bỏ lỡ chương trình {campaign.mail_subject} của chúng tôi!"
        )

        # Lấy danh sách email từ request payload
        email_list = request.data.get("email_list")
        print("request.data", request.data)
        if not email_list:  # => true
            mail_tracks = MailTrack.objects.filter(campaign=campaign)
            email_list = [
                mail_track.contact.user.email for mail_track in mail_tracks]

        from_email = None
        # Gửi email đến tất cả các email trong danh sách
        for recipient_email in email_list:
            contact = Contact.objects.get(user__email=recipient_email)
            mail_track = MailTrack.objects.get(
                contact=contact, campaign_id=campaign_id)
            track_id = mail_track.track_id
            html_content = f"""
                <html>
                <body>
                    <h2>{subject}</h2>
                    <p>{message}</p>
                    <a href="http://localhost:8000/email/click/{track_id}/">Xem ngay! Tại đây!</a>
                    {campaign.mail_content}
                    <div>
                        <img class="open-tracking-link" src="http:localhost:8000/email/open/{track_id}/img.gif" style="display:none;" alt="">
                    </div>
                </body>
                </html>
            """
            email = EmailMessage(subject, html_content,
                                 from_email, [recipient_email])
            email.content_subtype = "html"  # Đặt nội dung là HTML
            email.send()

            mail_track.is_send = True
            mail_track.save()
        return JsonResponse({"status": "HTML email sent successfully"})


class MailTrackAPIView(APIView):
    def get(self, request, track_id=None):
        """
        Fetch a single MailTrack by ID or list all MailTrack.
        """
        if track_id:
            try:
                item = MailTrack.objects.get(track_id=track_id)
                serializer = MailTrackSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except MailTrack.DoesNotExist:
                return Response(
                    {"error": "MailTrack not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            items = MailTrack.objects.all()
            serializer = MailTrackSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new MailTrack.
        """
        serializer = MailTrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(staff=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, track_id=None):
        try:
            item = MailTrack.objects.get(track_id=track_id)
        except MailTrack.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # `partial=True` allows partial updates
        serializer = MailTrackSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, track_id=None):
        """
        Delete a item by ID.
        """
        try:
            item = MailTrack.objects.get(track_id=track_id)
            item.delete()
            return Response(
                {"message": "MailTrack deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "MailTrack not found"}, status=status.HTTP_404_NOT_FOUND
            )


def track_open_email(request, track_id):
    mail_track = MailTrack.objects.get(track_id=track_id)
    mail_track.is_open = True
    mail_track.save()

    # Trả về một hình ảnh pixel (1x1)
    image_data = base64.b64decode(
        "R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==")
    return HttpResponse(image_data, content_type="image/gif")


def track_click(request, track_id):
    mail_track = MailTrack.objects.get(track_id=track_id)
    mail_track.is_open = True
    mail_track.is_click = True
    mail_track.save()
    return HttpResponse("Chào mừng đến với siêu ưu đãi!", status=200)


def track_unsubscribe(request, track_id):
    mail_track = MailTrack.objects.get(track_id=track_id)
    mail_track.is_unsubscribe = True
    mail_track.save()
    return HttpResponse("Unsubscribed", status=200)
