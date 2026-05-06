# Generated manually for security event logging.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0061_featuredpost_period_end_score"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SecurityEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("username", models.CharField(blank=True, default="", max_length=150)),
                ("event_type", models.CharField(choices=[("login_success", "Uspješna prijava"), ("login_failed", "Neuspješna prijava"), ("login_lockout", "Blokirana prijava"), ("registration_success", "Uspješna registracija"), ("registration_blocked", "Blokirana registracija"), ("turnstile_failed", "Turnstile nije prošao"), ("activation_success", "Račun aktiviran"), ("activation_failed", "Neuspješna aktivacija"), ("resend_email_success", "Ponovno poslan email"), ("resend_email_blocked", "Blokirano ponovno slanje emaila"), ("password_change_success", "Lozinka promijenjena"), ("password_change_failed", "Neuspješna promjena lozinke"), ("email_change_requested", "Zatražena promjena emaila"), ("email_change_confirmed", "Email potvrđen"), ("comment_rate_limited", "Komentiranje ograničeno"), ("duplicate_comment_blocked", "Dupli komentar blokiran"), ("post_deleted", "Post izbrisan"), ("avatar_deleted", "Avatar izbrisan"), ("suspicious_access", "Sumnjiv pristup")], max_length=60)),
                ("severity", models.CharField(choices=[("info", "Info"), ("warning", "Upozorenje"), ("critical", "Kritično")], default="info", max_length=20)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.CharField(blank=True, default="", max_length=255)),
                ("path", models.CharField(blank=True, default="", max_length=255)),
                ("method", models.CharField(blank=True, default="", max_length=10)),
                ("message", models.TextField(blank=True, default="")),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="security_events", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["event_type", "created_at"], name="blog_securi_event_t_4a6a7a_idx"),
                    models.Index(fields=["severity", "created_at"], name="blog_securi_severit_f0c1e2_idx"),
                    models.Index(fields=["user", "created_at"], name="blog_securi_user_id_fef7bf_idx"),
                    models.Index(fields=["ip_address", "created_at"], name="blog_securi_ip_addr_3e76e9_idx"),
                ],
            },
        ),
    ]
