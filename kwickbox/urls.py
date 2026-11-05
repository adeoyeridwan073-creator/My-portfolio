from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from contact.views import contact_submit


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="portfolio.html"), name="portfolio"),
    path("contact/", contact_submit, name="contact_submit"),
]
