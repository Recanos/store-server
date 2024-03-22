from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [BasketAdmin, ]
    search_fields = ['username']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'created', 'expiration']
    fields = ['code', 'user', 'created', 'expiration']
    readonly_fields = ['created']
