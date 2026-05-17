from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import ApprovedEmail, AccessRequest, BugReport
from .forms import EmailCheckForm, AccessRequestForm, BugReportForm


def home(request):
    form = EmailCheckForm()
    return render(request, 'distribution/home.html', {
        'form': form,
        'apk_version': settings.APK_VERSION,
    })


def check_email(request):
    if request.method != 'POST':
        return redirect('home')

    form = EmailCheckForm(request.POST)
    if not form.is_valid():
        return render(request, 'distribution/home.html', {
            'form': form,
            'apk_version': settings.APK_VERSION,
            'scroll_to_download': True,
        })

    email = form.cleaned_data['email']

    if ApprovedEmail.objects.filter(email=email).exists():
        request.session['approved_email'] = email
        return redirect('download')

    try:
        req = AccessRequest.objects.get(email=email)
        if req.status == AccessRequest.STATUS_APPROVED:
            ApprovedEmail.objects.get_or_create(email=email)
            request.session['approved_email'] = email
            return redirect('download')
        elif req.status == AccessRequest.STATUS_PENDING:
            return redirect('applied_pending')
        else:
            return render(request, 'distribution/home.html', {
                'form': form,
                'apk_version': settings.APK_VERSION,
                'scroll_to_download': True,
                'access_error': (
                    'Your access request was not approved. '
                    'Email belmontsolutionsgh@gmail.com for more information.'
                ),
            })
    except AccessRequest.DoesNotExist:
        pass

    return redirect(f'/apply/?email={email}')


def apply(request):
    initial_email = request.GET.get('email', '')

    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if ApprovedEmail.objects.filter(email=email).exists():
                request.session['approved_email'] = email
                return redirect('download')
            if AccessRequest.objects.filter(email=email).exists():
                return redirect('applied_pending')
            form.save()
            return redirect('applied_pending')
    else:
        form = AccessRequestForm(initial={'email': initial_email})

    return render(request, 'distribution/apply.html', {'form': form})


def applied_pending(request):
    return render(request, 'distribution/applied.html')


def download(request):
    if not request.session.get('approved_email'):
        messages.warning(request, 'Please verify your email to access the download.')
        return redirect('home')

    return render(request, 'distribution/download.html', {
        'apk_url': settings.APK_URL,
        'apk_filename': settings.APK_FILENAME,
        'apk_version': settings.APK_VERSION,
        'email': request.session.get('approved_email'),
    })


def report_bug(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bug_reported')
    else:
        initial = {}
        if request.session.get('approved_email'):
            initial['reporter_email'] = request.session['approved_email']
        form = BugReportForm(initial=initial)

    return render(request, 'distribution/bug_report.html', {'form': form})


def bug_reported(request):
    return render(request, 'distribution/bug_reported.html')
