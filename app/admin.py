from django.contrib import admin

from .models import feedback_content, account_settings

# Register your models here.
admin.site.register(feedback_content)
admin.site.register(account_settings)
