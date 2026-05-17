from django.contrib import admin
from django.utils.html import format_html
from .models import ApprovedEmail, AccessRequest, BugReport


@admin.register(ApprovedEmail)
class ApprovedEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'note', 'added_at']
    search_fields = ['email']
    ordering = ['email']


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'institution', 'status_badge', 'created_at', 'reviewed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['email', 'name', 'institution']
    readonly_fields = ['created_at', 'reviewed_at']
    actions = ['approve_requests', 'reject_requests']

    def status_badge(self, obj):
        colors = {
            'pending': '#f5a623',
            'approved': '#34a853',
            'rejected': '#d93025',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:4px;font-size:12px;font-weight:600">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='Approve selected requests and notify users by email')
    def approve_requests(self, request, queryset):
        count = 0
        for req in queryset.filter(status=AccessRequest.STATUS_PENDING):
            req.approve()
            count += 1
        self.message_user(request, f'{count} request(s) approved, added to whitelist, users notified.')

    @admin.action(description='Reject selected requests')
    def reject_requests(self, request, queryset):
        count = 0
        for req in queryset.filter(status=AccessRequest.STATUS_PENDING):
            req.reject()
            count += 1
        self.message_user(request, f'{count} request(s) rejected.')


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'reporter_email', 'severity_badge', 'status_badge', 'app_version', 'device_model', 'screenshot_thumb', 'created_at']
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['title', 'reporter_email', 'reporter_name', 'description']
    readonly_fields = ['created_at', 'screenshot_preview']
    fieldsets = [
        ('Reporter', {'fields': ['reporter_name', 'reporter_email']}),
        ('Bug Details', {'fields': ['title', 'severity', 'description', 'steps_to_reproduce']}),
        ('Environment', {'fields': ['app_version', 'device_model']}),
        ('Screenshot', {'fields': ['screenshot', 'screenshot_preview']}),
        ('Admin', {'fields': ['status', 'admin_notes', 'created_at']}),
    ]

    def severity_badge(self, obj):
        colors = {
            'low': '#34a853',
            'medium': '#f5a623',
            'high': '#ff6b35',
            'critical': '#d93025',
        }
        label = obj.get_severity_display().split(' — ')[0]
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:600">{}</span>',
            colors.get(obj.severity, '#999'), label
        )
    severity_badge.short_description = 'Severity'

    def status_badge(self, obj):
        colors = {
            'new': '#4a6cf7',
            'in_progress': '#f5a623',
            'resolved': '#34a853',
            'wont_fix': '#888',
        }
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:600">{}</span>',
            colors.get(obj.status, '#999'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def screenshot_thumb(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;cursor:pointer;" />', obj.screenshot.url)
        return '—'
    screenshot_thumb.short_description = 'Screenshot'

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width:700px;max-height:500px;border-radius:8px;border:1px solid #ddd;" /></a>',
                obj.screenshot.url, obj.screenshot.url
            )
        return '—'
    screenshot_preview.short_description = 'Screenshot Preview'
