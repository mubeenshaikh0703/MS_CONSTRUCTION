from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum
from accounts.models import Profile


from .models import ContactMessage
from booking.models import House, Booking, Payment


def home(request):
    bookings = []
    payments = []

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(
            user=request.user
        ).select_related('house')

        payments = Payment.objects.filter(
            booking__user=request.user
        ).select_related('booking', 'booking__house').order_by('-paid_on')[:5]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            return redirect('home')

    return render(request, 'core/home.html', {
        'bookings': bookings,
        'payments': payments
    })


@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_houses = House.objects.count()
    total_bookings = Booking.objects.count()

    status_counts = {
        'pending': Booking.objects.filter(status='PENDING').count(),
        'approved': Booking.objects.filter(status='APPROVED').count(),
        'in_progress': Booking.objects.filter(status='IN_PROGRESS').count(),
        'completed': Booking.objects.filter(status='COMPLETED').count(),
        'cancelled': Booking.objects.filter(status='CANCELLED').count(),
    }

    total_revenue = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_users': total_users,
        'total_houses': total_houses,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        **status_counts
    }

    return render(request, 'core/admin_dashboard.html', context)
