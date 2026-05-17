from django import forms
from .models import AccessRequest, BugReport


class EmailCheckForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
        })
    )

    def clean_email(self):
        return self.cleaned_data['email'].lower().strip()


class AccessRequestForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ['name', 'email', 'institution', 'reason']
        labels = {
            'institution': 'Hospital / Clinic / Organization (optional)',
            'reason': 'Why do you want to use iSpeye?',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr. Jane Doe',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Korle Bu Teaching Hospital',
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Briefly describe your use case...',
            }),
        }

    def clean_email(self):
        return self.cleaned_data['email'].lower().strip()


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['reporter_name', 'reporter_email', 'title', 'severity',
                  'description', 'steps_to_reproduce', 'device_model', 'screenshot']
        labels = {
            'reporter_name': 'Your Name',
            'reporter_email': 'Your Email',
            'title': 'Bug Title',
            'severity': 'Severity',
            'description': 'What happened?',
            'steps_to_reproduce': 'Steps to Reproduce (optional)',
            'device_model': 'Device Model (optional)',
            'screenshot': 'Screenshot (optional)',
        }
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jane Doe'}),
            'reporter_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. App crashes when uploading a photo'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what happened clearly...'}),
            'steps_to_reproduce': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '1. Open app\n2. Tap Upload\n3. App crashes'}),
            'device_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Samsung Galaxy A54'}),
            'screenshot': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
