# from datetime import timezone
# from django.conf import settings
# from django.contrib.auth import get_user_model
# # Nhập mô-đun models từ Django để định nghĩa các mô hình cơ sở dữ liệu
# from django.db import models
# from django.contrib import auth
# from django.contrib.auth.models import AbstractUser, Group  # Thêm Group vào đây

# # Class User - supertype


# class CustomUser(AbstractUser):
#     # Đặt tên bảng tùy chỉnh)
#     groups = models.ManyToManyField(Group, related_name="custom_users")

#     def __str__(self):
#         return self.username


# class Staff(models.Model):
#     Position = models.CharField(max_length=100,
#                                 choices=[
#                                     ('Sales', 'Sales'),
#                                     ('Order Manager', 'Order Manager'),
#                                     ('Service Issue Handler',
#                                      'Service Issue Handler'),
#                                     ('Contact Manager', 'Contact Manager'),
#                                     ('Order Issue Handler', 'Order Issue Handler'),
#                                 ])
#     StaffID = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, related_name='staffs')

#     def __str__(self):
#         return self.StaffID.username


# class Contact(models.Model):
#     LifecycleStage = models.CharField(
#         max_length=50,  # Độ dài tối đa cho tên nhà xuất bản
#         choices=[
#             ('Subscriber', 'Subscriber'),
#             ('Lead', 'Lead'),
#             ('Opportunity', 'Opportunity'),
#             ('Customer', 'Customer'),
#             ('Evangelist', 'Evangelist')
#         ])
#     Address = models.CharField(max_length=200)
#     PhoneNumber = models.CharField(max_length=20)
#     ContactID = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, related_name='contacts')
#     StaffInCharged = models.ForeignKey(
#         Staff, on_delete=models.CASCADE, related_name='contacts')

#     def __str__(self):
#         return self.ContactID.username


# class Order(models.Model):
#     StatusChoices = (
#         ('Pending', 'Pending'),
#         ('On Delivery', 'On Delivery'),
#         ('Delivered', 'Delivered'),
#         ('Returned', 'Returned'),
#     )
#     OrderID = models.AutoField(primary_key=True)
#     CreatedDate = models.DateField(auto_now_add=True)
#     Status = models.CharField(max_length=50, choices=StatusChoices)
#     TotalPrice = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0)
#     ContactName = models.ForeignKey(
#         Contact, on_delete=models.CASCADE, related_name='orders')
#     StaffName = models.ForeignKey(
#         Staff, on_delete=models.CASCADE, related_name='orders')

#     def save(self, *args, **kwargs):
#         # Tính tổng giá tiền của đơn hàng từ OrderDetail
#         total_amount = 0
#         # Lấy tất cả OrderDetail liên kết với Order này
#         order_details = self.orderdetail_set.all()
#         for detail in order_details:
#             total_amount += detail.Quantity * detail.ProductID.UnitPrice
#         self.TotalPrice = total_amount

#         # Gọi save() của superclass để lưu đối tượng Order
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Order {self.OrderID}"

# # 7. Ticket Model


# class Ticket(models.Model):
#     class TicketPriority(models.TextChoices):
#         LOW = 'LOW', 'Low'
#         MEDIUM = 'MEDIUM', 'Medium'
#         HIGH = 'HIGH', 'High'

#     class TicketStatus(models.TextChoices):
#         NEW = 'NEW', 'New'
#         WAITING_ON_CONTACT = 'WAITING_ON_CONTACT', 'Waiting On Contact'
#         IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
#         CLOSED = 'CLOSED', 'Closed'
#         SOLVED = 'SOLVED', 'Solved'

#     class TicketSubject(models.TextChoices):
#         ORDER_ISSUE = 'ORDER_ISSUE', 'Order Issue'
#         SERVICE_ISSUE = 'SERVICE_ISSUE', 'Service Issue'

#     ticket_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=250)
#     description = models.TextField()
#     subject = models.CharField(max_length=100, choices=TicketSubject.choices)
#     created_date = models.DateField(auto_now_add=True)
#     closed_date = models.DateField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=TicketStatus.choices)
#     priority = models.CharField(max_length=10, choices=TicketPriority.choices)
#     contact_name = models.ForeignKey(
#         Contact, on_delete=models.CASCADE, related_name='tickets')

# # class Ticket(models.Model):
# #     # Lựa chọn cho Priority
# #     PriorityChoices = [
# #         ('Low', 'Low'),
# #         ('Medium', 'Medium'),
# #         ('High', 'High'),
# #     ]

# #     # Lựa chọn cho Status
# #     StatusChoices = [
# #         ('New', 'New'),
# #         ('Waiting On Contact', 'Waiting On Contact'),
# #         ('In Progress', 'In Progress'),
# #         ('Closed', 'Closed'),
# #         ('Solved', 'Solved'),
# #     ]

# #     # Lựa chọn cho Subject
# #     SubjectChoices = [
# #         ('Order Issue', 'Order Issue'),
# #         ('Service Issue', 'Service Issue'),
# #     ]

# #     # Các trường của Ticket
# #     TicketID = models.AutoField(primary_key=True)
# #     Title = models.CharField(max_length=250)
# #     Description = models.TextField()
# #     Subject = models.CharField(max_length=100, choices=SubjectChoices)
# #     CreatedDate = models.DateTimeField(auto_now_add=True)
# #     CloseDate = models.DateField(null=True, blank=True)
# #     Status = models.CharField(
# #         max_length=20, choices=StatusChoices, default='New')
# #     Priority = models.CharField(max_length=10, choices=PriorityChoices)

# #     OrderID = models.ForeignKey(
# #         Order, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
# #     User = models.ForeignKey(settings.AUTH_USER_MODEL,
# #                              on_delete=models.CASCADE, null=True, blank=True)

#     # # Override phương thức save để tự động điền UserID
#     # def save(self, *args, **kwargs):
#     #     # Kiểm tra nếu ticket có chủ đề "Service Issue" hoặc "Order Issue" và gán người xử lý tương ứng
#     #     if self.Subject == 'Service Issue':
#     #         handler = Staff.objects.filter(
#     #             Position='Service Issue Handler').first()
#     #     elif self.Subject == 'Order Issue':
#     #         handler = Staff.objects.filter(
#     #             Position='Order Issue Handler').first()
#     #     else:
#     #         handler = None

#     #     # Gán StaffName nếu tìm được handler
#     #     if handler:
#     #         self.StaffName = handler

#     #     if self.Status == 'Closed' and not self.CloseDate:
#     #         # Automatically set CloseDate when ticket is closed
#     #         self.CloseDate = timezone.now().date()

#     #     # Gọi phương thức save của superclass để lưu dữ liệu
#     #     super().save(*args, **kwargs)

#     # def __str__(self):
#     #     return f"Ticket - {self.Subject} ({self.Status})"


# class Product(models.Model):
#     ProductID = models.AutoField(primary_key=True)
#     ProductName = models.CharField(max_length=100)
#     Unit = models.CharField(max_length=50)
#     UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.ProductName


# class OrderDetail(models.Model):
#     OrderID = models.ForeignKey(Order, on_delete=models.CASCADE)
#     ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
#     Quantity = models.IntegerField()
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         unique_together = (('OrderID', 'ProductID'),)  # Đặt khóa chính kết hợp

#     def __str__(self):
#         return f"OrderDetail for Order {self.OrderID.OrderID} - Product {self.ProductID.ProductName}"

#     def save(self, *args, **kwargs):
#         # Cập nhật subtotal trước khi lưu
#         self.subtotal = self.ProductID.UnitPrice * self.Quantity
#         super().save(*args, **kwargs)
# # model chatpoll


# class ChatPoll(models.Model):
#     ChatPollID = models.AutoField(primary_key=True)
#     Timestamp = models.DateTimeField(auto_now_add=True)
#     Message = models.TextField()
#     Sender = models.ForeignKey(
#         Contact, on_delete=models.CASCADE, related_name="chat_polls")
#     Receiver = models.ForeignKey(
#         Staff, on_delete=models.CASCADE, related_name="chat_polls")

#     class Meta:
#         ordering = ['Timestamp']

#     def __str__(self):
#         return f"Chat between {self.Sender} and {self.Receiver}"
