from django.shortcuts import render, redirect
from .forms.register_form import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from admin_manager.models import Product, Ticket
from .forms.add_ticket_form import TicketForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(">user", user)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_staff:
                return redirect('/system-admin/')
            else:
                # Ngược lại chuyển hướng đến trang /products
                return redirect('/products/')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def custom_logout(request):
    logout(request)  # This logs out the user
    return redirect('login')  # Redirect to the login page after logout


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("form", form)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to the login page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# View for displaying and adding a new ticket


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assign the logged-in user to the ticket
            ticket.save()
            # Redirect to ticket list after creation
            return redirect('ticket_list')
    else:
        form = TicketForm()

    return render(request, 'ticket/create_ticket.html', {'form': form})

# View for listing the tickets created by the logged-in user


@login_required
def ticket_list(request):
    # Get tickets only for the logged-in user
    tickets = Ticket.objects.filter(User=request.user)
    return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


# @login_required
def product_list(request):

    # Queries all products from the database
    products = Product.objects.all()

    # Format UnitPrice to the desired format
    for product in products:
        product.unit_price = "{:,.0f}".format(
            product.unit_price)  # Example: 100,000.000
    return render(request, 'products.html', {'product_list': products})
