from django.db import models
from django.utils import timezone


class ApprovedEmail(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    note = models.CharField(max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']
        verbose_name = 'Approved Email'
        verbose_name_plural = 'Approved Emails'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)


class AccessRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)
    institution = models.CharField(max_length=200, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer_note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Access Request'
        verbose_name_plural = 'Access Requests'

    def __str__(self):
        return f'{self.email} ({self.status})'

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def approve(self, note=''):
        from django.conf import settings
        from django.core.mail import send_mail

        self.status = self.STATUS_APPROVED
        self.reviewed_at = timezone.now()
        self.reviewer_note = note
        self.save()

        ApprovedEmail.objects.get_or_create(
            email=self.email,
            defaults={'note': f'Approved from access request #{self.pk}'}
        )

        send_mail(
            subject="You've been approved to download iSpeye",
            message=(
                f"Hi {self.name},\n\n"
                "Great news! Your request to access iSpeye has been approved.\n\n"
                f"To download, visit:\n{settings.APP_BASE_URL}\n\n"
                "Enter your email address on the page and you'll be taken straight to the download.\n\n"
                "iSpeye is a research-stage AI screening tool and is NOT a medical device.\n"
                "Always consult a qualified healthcare professional for medical advice.\n\n"
                "— Belmont Solutions"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=True,
        )

    def reject(self, note=''):
        self.status = self.STATUS_REJECTED
        self.reviewed_at = timezone.now()
        self.reviewer_note = note
        self.save()


class BugReport(models.Model):
    SEVERITY_LOW = 'low'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_HIGH = 'high'
    SEVERITY_CRITICAL = 'critical'
    SEVERITY_CHOICES = [
        (SEVERITY_LOW, 'Low — Minor inconvenience'),
        (SEVERITY_MEDIUM, 'Medium — Feature not working'),
        (SEVERITY_HIGH, 'High — App crashes'),
        (SEVERITY_CRITICAL, 'Critical — Data loss / security issue'),
    ]

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_WONT_FIX = 'wont_fix'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_RESOLVED, 'Resolved'),
        (STATUS_WONT_FIX, "Won't Fix"),
    ]

    reporter_name = models.CharField(max_length=150)
    reporter_email = models.EmailField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps_to_reproduce = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default=SEVERITY_MEDIUM)
    app_version = models.CharField(max_length=20, blank=True, default='1.3.1')
    device_model = models.CharField(max_length=100, blank=True)
    screenshot = models.ImageField(upload_to='bug_reports/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bug Report'
        verbose_name_plural = 'Bug Reports'

    def __str__(self):
        return f'[{self.get_severity_display().split(" — ")[0]}] {self.title}'
