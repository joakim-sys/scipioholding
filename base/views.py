from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

from django.views import generic

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            subject = form.cleaned_data["subject"]
            comment = form.cleaned_data["message"]

            emailFrom = form.cleaned_data["email"]
            emailTo = [settings.EMAIL_HOST_USER]

            message = f"Sender: {emailFrom}\nName: {name}\nSubject: {subject}\nComment: {comment}"

            send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
            return redirect("success")

    form = ContactForm()
    return render(request, "home/home_page.html")

class Success(generic.TemplateView):
    template_name = 'base/success.html'