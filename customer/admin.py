# from django.contrib import admin
# from .models import (
#     CustomUser, Staff, Contact, Order, Ticket, Product, OrderDetail, ChatPoll
# )
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group

# # Tùy chỉnh hiển thị cho CustomUser
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active', 'groups')
#     search_fields = ('username', 'email')
#     ordering = ('username',)

#     # Sao chép các fieldsets từ UserAdmin, không thêm trùng lặp
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )


# admin.site.register(CustomUser, CustomUserAdmin)


# # Tùy chỉnh hiển thị cho Staff
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('StaffID', 'Position')
#     list_filter = ('Position',)
#     search_fields = ('StaffID__username', 'Position')

# admin.site.register(Staff, StaffAdmin)


# # Tùy chỉnh hiển thị cho Contact
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('ContactID', 'LifecycleStage', 'PhoneNumber', 'Address', 'StaffInCharged')
#     list_filter = ('LifecycleStage',)
#     search_fields = ('ContactID__username', 'PhoneNumber', 'Address')

# admin.site.register(Contact, ContactAdmin)


# # Tùy chỉnh hiển thị cho Order
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('OrderID', 'CreatedDate', 'Status', 'TotalPrice', 'ContactName', 'StaffName')
#     list_filter = ('Status', 'CreatedDate')
#     search_fields = ('ContactName__ContactID__username', 'StaffName__StaffID__username')

# admin.site.register(Order, OrderAdmin)


# # Tùy chỉnh hiển thị cho Ticket
# class TicketAdmin(admin.ModelAdmin):
#     # list_display = ('TicketID', 'Title', 'Subject', 'Status', 'Priority', 'CreatedDate', 'CloseDate', 'ContactName', 'StaffName', 'OrderID')
#     list_display = ('TicketID', 'Title', 'Subject', 'Status', 'Priority', 'CreatedDate', 'CloseDate', 'OrderID')
#     list_filter = ('Status', 'Priority', 'Subject')
#     # search_fields = ('Title', 'Description', 'ContactName__ContactID__username', 'StaffName__StaffID__username')
#     search_fields = ('Title', 'Description')
#     date_hierarchy = 'CreatedDate'

# admin.site.register(Ticket, TicketAdmin)


# # Tùy chỉnh hiển thị cho Product
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('ProductID', 'ProductName', 'Unit', 'UnitPrice')
#     search_fields = ('ProductName',)

# admin.site.register(Product, ProductAdmin)


# # Tùy chỉnh hiển thị cho OrderDetail
# class OrderDetailAdmin(admin.ModelAdmin):
#     list_display = ('OrderID', 'ProductID', 'Quantity')
#     search_fields = ('OrderID__OrderID', 'ProductID__ProductName')

# admin.site.register(OrderDetail, OrderDetailAdmin)


# # Tùy chỉnh hiển thị cho ChatPoll
# class ChatPollAdmin(admin.ModelAdmin):
#     list_display = ('ChatPollID', 'Timestamp', 'Message', 'Sender', 'Receiver')
#     search_fields = ('Message', 'Sender__ContactID__username', 'Receiver__StaffID__username')
#     list_filter = ('Timestamp',)
#     date_hierarchy = 'Timestamp'

# admin.site.register(ChatPoll, ChatPollAdmin)

# # Xóa bỏ hiển thị mặc định của Group
# # admin.site.unregister(Group)
