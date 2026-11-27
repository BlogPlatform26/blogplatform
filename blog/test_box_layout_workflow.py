import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import UserBox


class BoxLayoutWorkflowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="layout-owner")
        self.client.force_login(self.owner)
        self.boxes = [UserBox.objects.create(user=self.owner, title=f"Box {i}",
                      position="left" if i < 3 else "right", order=i % 3) for i in range(6)]
        self.url = reverse("blog_settings") + "?tab=boxevi"

    def layout(self):
        return [{"id": b.pk, "position": b.position} for b in self.boxes]

    def post(self, layout):
        return self.client.post(self.url, {"save_box_layout": "1", "box_layout_json": json.dumps(layout)},
                                HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def saved(self):
        return list(UserBox.objects.filter(user=self.owner).order_by("id").values_list("id", "position", "order"))

    def test_reorder_and_full_side_swap_acknowledge_persisted_layout(self):
        layout = self.layout()
        layout[0]["position"], layout[3]["position"] = "right", "left"
        layout[1], layout[2] = layout[2], layout[1]
        response = self.post(layout)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["saved"])
        self.assertEqual(response.json()["layout"], layout)
        self.assertEqual(list(UserBox.objects.filter(user=self.owner, position="left").order_by("order").values_list("id", flat=True)),
                         [self.boxes[2].pk, self.boxes[1].pk, self.boxes[3].pk])

    def test_invalid_and_stale_layouts_never_report_success_or_write(self):
        original = self.saved()
        other = get_user_model().objects.create_user(username="other-layout-owner")
        foreign = UserBox.objects.create(user=other, title="Foreign box", position="left", order=0)
        cases = [None, {}, self.layout()[:-1], self.layout() + [self.layout()[0]],
                 [{**item, "position": "left"} for item in self.layout()],
                 [{"id": 999999, "position": "left"}] + self.layout()[1:],
                 [{"id": foreign.pk, "position": "left"}] + self.layout()[1:],
                 [{**self.layout()[0], "position": []}] + self.layout()[1:],
                 [{**self.layout()[0], "id": True}] + self.layout()[1:]]
        for layout in cases:
            with self.subTest(layout=layout):
                response = self.post(layout)
                self.assertIn(response.status_code, (400, 409))
                self.assertFalse(response.json()["saved"])
                self.assertTrue(response.json()["error"])
                self.assertEqual(self.saved(), original)

    def test_malformed_json_returns_error_not_redirect(self):
        response = self.client.post(self.url, {"save_box_layout": "1", "box_layout_json": "["},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["saved"])

    def test_html_submission_still_redirects_to_active_box(self):
        response = self.client.post(self.url, {"save_box_layout": "1", "box_layout_json": json.dumps(self.layout()),
                                              "active_box_id": self.boxes[0].pk})
        self.assertRedirects(response, f"/blog/settings/?tab=boxevi&box={self.boxes[0].pk}", fetch_redirect_response=False)

    def test_failed_second_update_rolls_back_entire_layout(self):
        from django.db.models.query import QuerySet
        original = self.saved()
        layout = self.layout()
        layout[0]["position"], layout[3]["position"] = "right", "left"
        real_update = QuerySet.update
        calls = 0
        def fail_second(queryset, **kwargs):
            nonlocal calls
            if queryset.model is UserBox and "position" in kwargs:
                calls += 1
                if calls == 2:
                    raise RuntimeError("Synthetic save failure")
            return real_update(queryset, **kwargs)
        with patch.object(QuerySet, "update", fail_second):
            with self.assertRaises(RuntimeError):
                self.post(layout)
        self.assertEqual(self.saved(), original)
