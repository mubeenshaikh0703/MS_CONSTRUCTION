from django.contrib import admin
from .models import House, HouseImage, Booking, Payment


# -------------------------
# HOUSE IMAGE INLINE (Gallery)
# -------------------------
class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 2


# -------------------------
# HOUSE ADMIN
# -------------------------
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'house_type', 'price')
    list_filter = ('house_type',)
    search_fields = ('name',)
    inlines = [HouseImageInline]


# -------------------------
# BOOKING ADMIN
# -------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'house', 'status', 'start_date')
    list_filter = ('status',)
    search_fields = ('user__username', 'house__name')
    list_editable = ('status',)


# -------------------------
# PAYMENT ADMIN
# -------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_type', 'paid_on')
    list_filter = ('payment_type',)
    search_fields = ('booking__id', 'booking__user__username')
