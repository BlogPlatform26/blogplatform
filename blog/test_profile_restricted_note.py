from types import SimpleNamespace

from django.template import Context, Template
from django.test import SimpleTestCase


class ProfileRestrictedNoteTests(SimpleTestCase):
    template = Template(
        '{% include "blog/components/blog_profile_restricted_note.html" '
        'with restricted_note_class=note_class %}'
    )
    callers = {
        "magazin": "magazin-profile-note",
        "studio": "soho-profile-note",
        "shared": "blog-profile-panel__note",
    }
    message = (
        "Ovaj autor te je ograničio pa ne možeš pratiti, "
        "lajkati ni komentirati."
    )

    def render_note(self, note_class, user, blog, restricted):
        return self.template.render(
            Context(
                {
                    "request": SimpleNamespace(user=user),
                    "blog": blog,
                    "is_restricted": restricted,
                    "note_class": note_class,
                }
            )
        )

    def test_note_visibility_and_markup_for_all_callers(self):
        blog = SimpleNamespace(username="author", is_authenticated=True)
        scenarios = {
            "anonymous": (SimpleNamespace(is_authenticated=False), True, False),
            "owner": (blog, True, False),
            "unrestricted": (SimpleNamespace(is_authenticated=True), False, False),
            "restricted": (SimpleNamespace(is_authenticated=True), True, True),
        }

        for caller, note_class in self.callers.items():
            for scenario, (user, restricted, visible) in scenarios.items():
                with self.subTest(caller=caller, scenario=scenario):
                    rendered = self.render_note(note_class, user, blog, restricted)
                    if visible:
                        self.assertHTMLEqual(
                            rendered,
                            f'<div class="{note_class}">{self.message}</div>',
                        )
                    else:
                        self.assertEqual(rendered.strip(), "")
