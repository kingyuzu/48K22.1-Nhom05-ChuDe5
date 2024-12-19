from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class DepartmentChoices(models.TextChoices):
        CONTACT = '01', 'Contact'
        ORDER = '02', 'Order'
        SERVICE_ISSUE = '03', 'Service Issue'
        ORDER_ISSUE = '04', 'Order Issue'
        CAMPAIGN = '05', 'Campaign'

    class UserType(models.TextChoices):
        MANAGER = 'MANAGER', 'Manager'
        STAFF = 'STAFF', 'Staff'
        CUSTOMER = 'CUSTOMER', 'Customer'
    id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    department_code = models.CharField(
        max_length=2,
        choices=DepartmentChoices.choices,
        default=DepartmentChoices.CONTACT  # Mặc định là Contact
    )
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    created_date = models.DateTimeField(auto_now_add=True)
    date_join = models.DateField(auto_now_add=True)

    def get_department_name(self):
        return self.DepartmentChoices(self.department_code).label

    def __str__(self):
        return f"{self.username} ({self.get_department_name()})"

# 2. Contact Model


class Contact(models.Model):
    class LifecycleStage(models.TextChoices):
        SUBSCRIBER = 'SUBSCRIBER', 'Subscriber'
        LEAD = 'LEAD', 'Lead'
        OPPORTUNITY = 'OPPORTUNITY', 'Opportunity'
        EVANGELIST = 'EVANGELIST', 'Evangelist'
    # Không cần primary_key=True
    contact_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=LifecycleStage.choices
    )
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(
        User, related_name='contacts', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.contact_id:
            self.contact_id = f"KH{str(Contact.objects.count() + 1).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contact: {self.user.username}"


# 3. Staff Model
class Staff(models.Model):
    # Không cần primary_key=True
    staff_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            staff_count = Staff.objects.filter(
                user__department_code=self.user.department_code).count() + 1
            self.staff_id = f"NV{self.user.department_code}{str(staff_count).zfill(2)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Staff: {self.user.username}"


# 4. Order Model
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'NEW', 'New',
        CONFIRMED = 'CONFIRMED', 'Confirmed',
        IN_PROGRESS = 'IN_PROGRESS', 'In-Progress'
        DELIVERED = 'DELIVERED', 'Delivered'
        RETURNED = 'RETURNED', 'Returned'

    order_id = models.CharField(max_length=50, unique=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=OrderStatus.choices, max_length=50)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    contact_name = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='orders')
    staff_name = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='orders')

    def save(self, *args, **kwargs):
        if not self.order_id:
            order_count = Order.objects.count() + 1
            self.order_id = f"DH{str(order_count).zfill(3)}"
        super().save(*args, **kwargs)

    # def update_total_price(self):
    #     total_amount = sum(
    #         detail.subtotal for detail in self.orderdetail_set.all())
    #     self.total_price = total_amount
    #     self.save()

    def __str__(self):
        return f"Order {self.order_id}"


# 5. Product Model
class Product(models.Model):
    # SQLite > int , tự động tăng
    product_id = models.CharField(max_length=50, unique=True, blank=True)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            product_count = Product.objects.count() + 1
            self.product_id = f"P{str(product_count).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


# 6. OrderDetail Model
class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product_price = self.product.unit_price
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"OrderDetail for Order {self.order.order_id} - Product {self.product.product_name}"


# 7. Ticket Model
class Ticket(models.Model):
    class TicketPriority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class TicketStatus(models.TextChoices):
        NEW = 'NEW', 'New'
        WAITING_ON_CONTACT = 'WAITING_ON_CONTACT', 'Waiting On Contact'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CLOSED = 'CLOSED', 'Closed'
        SOLVED = 'SOLVED', 'Solved'

    class TicketSubject(models.TextChoices):
        ORDER_ISSUE = 'ORDER_ISSUE', 'Order Issue'
        SERVICE_ISSUE = 'SERVICE_ISSUE', 'Service Issue'

    ticket_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    subject = models.CharField(max_length=100, choices=TicketSubject.choices)
    created_date = models.DateTimeField(auto_now_add=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TicketStatus.choices)
    priority = models.CharField(max_length=10, choices=TicketPriority.choices)
    # contact_name = models.ForeignKey(
    #     Contact, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)


class Campaign(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        IN_PROGRESSED = 'IN_PROGRESSED', 'In progressed'
        CLOSED = 'CLOSED', 'Closed'

    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True, blank=True,
        related_name='campaigns'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    mail_subject = models.CharField(
        max_length=255, null=True, blank=True)  # New field
    mail_content = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.name} ({self.campaign_id})"


class MailTrack(models.Model):
    track_id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact,  # Assuming Contact model exists
        on_delete=models.CASCADE,
        related_name='mail_tracks'
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='mail_tracks'
    )
    is_send = models.BooleanField(default=False)  # Whether the mail was sent
    is_open = models.BooleanField(default=False)  # Whether the mail was opened
    # Whether any link in the mail was clicked
    is_click = models.BooleanField(default=False)
    # Whether the recipient unsubscribed
    is_unsubscribe = models.BooleanField(default=False)

    def __str__(self):
        return f"MailTrack {self.track_id} for Contact {self.contact_id} in Campaign {self.campaign_id}"
