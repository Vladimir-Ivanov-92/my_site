from django.contrib import admin

from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    readonly_fields = ['username', 'password']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['email_code', 'user', 'expiration']
    fields = ['email_code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
