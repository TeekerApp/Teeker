from django.contrib import admin

from .models import feedback_content, account_settings, Content

# Register your models here.
admin.site.register(feedback_content)
admin.site.register(account_settings)
admin.site.register(Content)
