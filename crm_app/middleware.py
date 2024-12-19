from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from admin_manager.models import User
from django.contrib.auth.models import AnonymousUser


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/products/'):
            print("request.user", request.user)
            if request.user and not isinstance(request.user, AnonymousUser) and request.user.user_type in [User.UserType.MANAGER, User.UserType.STAFF]:
                return redirect(reverse('admin-contact'))

        if request.path.startswith('/system-admin/'):
            if not request.user.is_authenticated:
                # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
                return redirect(reverse('login'))

            if request.user.user_type not in [User.UserType.MANAGER, User.UserType.STAFF]:
                # Trả về lỗi 403 nếu không phải Manager hoặc Staff
                return HttpResponseForbidden("Permission denied!")

        return self.get_response(request)
