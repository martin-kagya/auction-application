from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Item, Bid, Auction, Watchlist, Payment

# Create an inline admin class for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Payment)