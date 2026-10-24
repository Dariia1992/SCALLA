
from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):

    list_display = ("name","phone","email","is_read","status","created_at",)

    list_filter = ("is_read","status","created_at", )

    search_fields = ("name","phone","email","message",)

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

    actions = ("mark_as_read","mark_as_unread","mark_in_progress","mark_completed",)

    @admin.action(description="Mark as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    @admin.action(description="Mark as in progress")
    def mark_in_progress(self, request, queryset):
        queryset.update(status="in_progress")

    @admin.action(description="Mark as completed")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
