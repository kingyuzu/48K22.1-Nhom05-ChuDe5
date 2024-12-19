from django.contrib import admin
from .models import User, Staff, Contact, Order, Ticket, Product, OrderDetail
from django.contrib.auth.admin import UserAdmin

# CustomUser admin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number',
                    'first_name', 'last_name', 'address', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email')


admin.site.register(User, CustomUserAdmin)

# Staff admin
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('staff_id', 'hire_date')
#     list_filter = ('staff_id',)
#     search_fields = ('staff_id',)

# admin.site.register(Staff, StaffAdmin)

# Contact admin
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'user', 'address', 'lifecycle_stage')

admin.site.register(Contact, ContactAdmin)

# # Order admin
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('OrderID', 'CreatedDate', 'Status', 'get_total_price', 'get_contact_name', 'get_staff_name')
#     list_filter = ('Status', 'CreatedDate')  # Assuming these fields exist in your Order model.
#     search_fields = ('ContactName__ContactID__username', 'StaffName__StaffID__username')

#     def get_contact_name(self, obj):
#         return obj.ContactName.ContactID.username if obj.ContactName else '-'
#     get_contact_name.short_description = 'Contact Name'

#     def get_staff_name(self, obj):
#         return obj.StaffName.StaffID.username if obj.StaffName else '-'
#     get_staff_name.short_description = 'Staff Name'

#     def get_total_price(self, obj):
#         return obj.TotalPrice  # Assuming TotalPrice is a valid field in your Order model.
#     get_total_price.short_description = 'Total Price'

# admin.site.register(Order, OrderAdmin)

# # OrderDetail admin
# class OrderDetailAdmin(admin.ModelAdmin):
#     list_display = ('OrderID', 'ProductID', 'Quantity', 'get_total_price')

#     def get_total_price(self, obj):
#         return obj.Quantity * obj.ProductID.UnitPrice  # Assuming UnitPrice is a field in Product.
#     get_total_price.short_description = 'Total Price'

# admin.site.register(OrderDetail, OrderDetailAdmin)

# # Product admin
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('ProductID', 'ProductName', 'Unit', 'UnitPrice')  # Assuming these fields exist in your Product model.
#     search_fields = ('ProductID', 'ProductName')

# admin.site.register(Product, ProductAdmin)

# Ticket admin
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'title', 'subject', 'status', 'priority', 'created_date', 'closed_date', 'get_order_id')
    list_filter = ('status', 'priority', 'subject')  # Assuming these are valid fields in Ticket.
    date_hierarchy = 'created_date'  # Ensure CreatedDate is a valid field in your Ticket model.

    def get_order_id(self, obj):
        return obj.order.order_id if obj.order_id else '-'
    get_order_id.short_description = 'Order ID'

admin.site.register(Ticket, TicketAdmin)
