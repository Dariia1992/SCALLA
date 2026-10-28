
import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

from .models import ContactRequest
from .forms import ContactRequestForm


logger = logging.getLogger(__name__)


def home(request):

    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact = form.save()

        # Получаем данные из формы
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        # Проверяем заполнение полей
        if not all([name, email, phone, message]):
            messages.error(
                request,
                "Please fill in all fields."
            )
            return redirect("/#contacts")

        # Проверяем длину полей
        if len(name) > 100 or len(phone) > 20:
            messages.error(
                request,
                "Please check your details."
            )
            return redirect("/#contacts")

        # Проверяем email
        try:
            validate_email(email)

        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email."
            )
            return redirect("/#contacts")

        # 1. Сохраняем заявку в базе данных
        contact = ContactRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # 2. Отправляем уведомление на email
        try:
            send_mail(
                subject=f"New SCALLA Contact Request #{contact.id}",

                message=(
                    f"New request from SCALLA website\n\n"
                    f"Name: {name}\n"
                    f"Phone: {phone}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{message}"
                ),

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[settings.CONTACT_EMAIL],

                fail_silently=False
            )

        except Exception:
            logger.exception(
                "Email notification failed for request %s",
                contact.id
            )
            messages.warning(
                request,
                "Your request was saved, but email notification failed."
            )

        else:
            messages.success(
                request,
                "Your request has been submitted successfully!"
            )

        # Возвращаем клиента к форме
        return redirect("/#contacts")

    # Открываем главную страницу
    return render(request, "services/home.html")


def privacy_policy(request):
    return render(request, "services/privacy_policy.html")