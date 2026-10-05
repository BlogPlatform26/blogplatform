from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase88eForestPolarCalendarFitTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.forest = User.objects.create_user(username="phase88e-forest")
        cls.polar = User.objects.create_user(username="phase88e-polar")
        cls.post = Post.objects.create(author=cls.forest, title="Objava", content="<p>Sadrzaj</p>", status="published")

    def test_both_designs_render_local_tablet_calendar_contract(self):
        for author, template in ((self.forest, "sumska_svjetlost"), (self.polar, "polarna_svjetlost")):
            author.profile.template = template
            author.profile.save(update_fields=["template"])
            response = self.client.get(reverse("user_blog", args=[author.username]))
            content = response.content.decode(response.charset)
            self.assertIn("Phase 88e", content)
            self.assertIn("grid-template-columns: 44px minmax(0, 1fr) 44px", content)
            self.assertIn("repeat(7, minmax(0, 1fr)) !important", content)

    def test_other_design_does_not_receive_calendar_contract(self):
        self.forest.profile.template = "zlatni_horizont"
        self.forest.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.forest.username]))
        self.assertNotIn("Phase 88e", response.content.decode(response.charset))
