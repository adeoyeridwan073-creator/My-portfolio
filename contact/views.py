from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import ContactMessage


def _form_response(request, *, message=None, error=None, status=200):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        payload = {"error": error} if error else {"message": message}
        return JsonResponse(payload, status=status)

    if error:
        messages.error(request, error)
    else:
        messages.success(request, message)
    return redirect(f"{reverse('portfolio')}#contact")


@require_POST
def contact_submit(request):
    if request.POST.get("website", "").strip():
        return _form_response(request, message="Thanks! Your message has been received.", status=201)

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    company = request.POST.get("company", "").strip()
    budget = request.POST.get("budget", "").strip()
    message = request.POST.get("message", "").strip()

    if not name or not email or not message:
        return _form_response(request, error="Please complete all fields.", status=400)
    if len(name) > 120 or len(company) > 160 or len(message) > 5000:
        return _form_response(request, error="One or more fields are too long.", status=400)
    if budget not in {"", "under-5k", "5k-15k", "15k-40k", "40k-plus"}:
        return _form_response(request, error="Please select a valid budget range.", status=400)
    try:
        validate_email(email)
    except ValidationError:
        return _form_response(request, error="Please enter a valid email address.", status=400)

    contact = ContactMessage.objects.create(
        name=name,
        email=email,
        company=company,
        budget=budget,
        message=message,
    )

    send_mail(
        subject=f"New project inquiry from {name}",
        message=(
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Company: {contact.company or 'Not provided'}\n"
            f"Budget: {contact.budget or 'Not provided'}\n\n"
            f"Message:\n{contact.message}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL_RECIPIENT],
        fail_silently=False,
    )

    return _form_response(request, message="Thanks! Your message has been received.", status=201)
