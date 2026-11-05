from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage


class ContactSubmissionTests(TestCase):
    def test_portfolio_renders_contact_form_and_assets(self):
        response = self.client.get(reverse("portfolio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="preview-storefront"')
        self.assertContains(response, 'class="preview-dashboard"')
        self.assertContains(response, 'class="preview-landing"')
        self.assertContains(response, "Adeoye Ridwan")
        self.assertContains(response, "Founder of Kwickbox")
        self.assertContains(response, "Websites for")
        self.assertEqual(response.content.count(b"<h1"), 1)
        self.assertContains(response, "Dashboard concept preview")
        self.assertContains(response, "/static/adeoye-ridwan.jpeg")
        self.assertContains(response, 'aria-label="Social and contact links"')
        self.assertContains(response, "https://github.com/adeoyeridwan073-creator/my-repo")
        self.assertContains(response, "https://cdn.simpleicons.org/whatsapp/25D366")
        self.assertContains(response, 'action="/contact/"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, "/static/portfolio.css")
        self.assertContains(response, "/static/portfolio.js")

    def test_custom_quote_cta_targets_contact_form(self):
        response = self.client.get(reverse("portfolio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-focus-target="#contactForm"')
        self.assertContains(response, "Custom quote")

    def test_valid_submission_is_saved(self):
        response = self.client.post(
            reverse("contact_submit"),
            {"name": "Taylor", "email": "taylor@example.com", "message": "A project inquiry"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().email, "taylor@example.com")

    def test_invalid_submission_is_rejected(self):
        response = self.client.post(
            reverse("contact_submit"),
            {"name": "Taylor", "email": "not-an-email", "message": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_standard_submission_redirects_with_confirmation(self):
        response = self.client.post(
            reverse("contact_submit"),
            {"name": "Taylor", "email": "taylor@example.com", "message": "A project inquiry"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [("/#contact", 302)])
        self.assertContains(response, "Thanks! Your message has been received.")
        self.assertEqual(ContactMessage.objects.count(), 1)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        EMAIL_HOST_USER="sender@gmail.com",
        CONTACT_EMAIL_RECIPIENT="recipient@gmail.com",
    )
    def test_submission_sends_email_to_configured_recipient(self):
        response = self.client.post(
            reverse("contact_submit"),
            {
                "name": "Taylor",
                "email": "taylor@example.com",
                "message": "A project inquiry",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["recipient@gmail.com"])
        self.assertIn("A project inquiry", mail.outbox[0].body)

    def test_honeypot_submission_is_acknowledged_but_not_saved(self):
        response = self.client.post(
            reverse("contact_submit"),
            {"website": "spam.example"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Thanks! Your message has been received.")
        self.assertEqual(ContactMessage.objects.count(), 0)

