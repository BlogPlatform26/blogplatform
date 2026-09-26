from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ProfileEditMobileTargetsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="profile-mobile-owner",
            password="test-password",
        )

    def test_profile_edit_renders_mobile_only_touch_target_contract(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("edit_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="bp-profile-edit-form"')
        self.assertContains(response, "bp-profile-save")
        self.assertContains(response, "bp-profile-menu")
        self.assertContains(response, "@media (max-width: 600px)")
        self.assertContains(response, ".bp-profile-edit-form .form-control")
        self.assertContains(response, ".bp-profile-edit-form .bp-profile-save")
        self.assertContains(response, ".navbar .bp-profile-menu .dropdown-item")
        self.assertContains(response, "min-height: 44px;")
