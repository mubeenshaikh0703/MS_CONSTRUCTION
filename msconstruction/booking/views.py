from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from reportlab.pdfgen import canvas

from .models import House, Booking, Payment


def select_work(request):
    houses = House.objects.all()
    return render(request, 'booking/select_work.html', {
        'houses': houses
    })


@login_required
def booking_page(request, house_id):
    house = get_object_or_404(House, id=house_id)

    if request.method == 'POST':
        site_address = request.POST.get('site_address')
        start_date = request.POST.get('start_date')

        if not site_address or not start_date:
            messages.error(request, 'All fields are required.')
            return redirect('booking', house_id=house.id)

        booking = Booking.objects.create(
            user=request.user,
            house=house,
            site_address=site_address,
            start_date=start_date
        )

        messages.success(request, 'Booking created successfully.')
        return redirect('payment', booking_id=booking.id)

    return render(request, 'booking/booking.html', {
        'house': house
    })


@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    total_paid = booking.total_paid()
    remaining = booking.house.price - total_paid

    if remaining <= 0:
        messages.info(request, 'This booking is already fully paid.')
        return redirect('payment_history')

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        amount = int(request.POST.get('amount', 0))

        if amount <= 0 or amount > remaining:
            messages.error(
                request,
                f'Invalid amount. Remaining balance is ₹{remaining}.'
            )
            return redirect('payment', booking_id=booking.id)

        Payment.objects.create(
            booking=booking,
            payment_type=payment_type,
            amount=amount
        )

        messages.success(request, 'Payment successful.')
        return redirect('payment_history')

    return render(request, 'booking/payment.html', {
        'booking': booking,
        'remaining': remaining
    })


@login_required
def payment_history(request):
    payments = Payment.objects.filter(
        booking__user=request.user
    ).select_related('booking', 'booking__house').order_by('-paid_on')

    return render(request, 'booking/payment_history.html', {
        'payments': payments
    })


@login_required
def invoice_pdf(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        booking__user=request.user
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="invoice_{payment.id}.pdf"'
    )

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    lines = [
        "MS CONSTRUCTION",
        "Payment Invoice",
        "",
        f"Invoice ID: {payment.id}",
        f"Booking ID: {payment.booking.id}",
        f"House: {payment.booking.house.name}",
        f"Amount Paid: ₹{payment.amount}",
        f"Payment Type: {payment.payment_type}",
        f"Date: {payment.paid_on.strftime('%d-%m-%Y')}",
        "",
        "Thank you for choosing MS Construction"
    ]

    for line in lines:
        p.drawString(50, y, line)
        y -= 20

    p.showPage()
    p.save()
    return response


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status in ['COMPLETED', 'CANCELLED']:
        messages.error(request, 'This booking cannot be cancelled.')
    else:
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, 'Booking cancelled.')

    return redirect('home')


def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'booking/house_detail.html', {
        'house': house
    })
