from django.urls import path
from . import views

urlpatterns = [
    path('select-work/', views.select_work, name='select_work'),

    path('booking/<int:house_id>/', views.booking_page, name='booking'),

    path('payment/<int:booking_id>/', views.payment_page, name='payment'),

    path('payments/', views.payment_history, name='payment_history'),

    path('invoice/<int:payment_id>/', views.invoice_pdf, name='invoice_pdf'),

    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('house/<int:house_id>/', views.house_detail, name='house_detail'),
]
