from html.parser import HTMLParser
from types import SimpleNamespace

from django.template import Context, Template
from django.test import SimpleTestCase


class ActionHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.text.append(value)


class ProfileInteractionActionsTests(SimpleTestCase):
    template = Template(
        '{% include "blog/components/blog_profile_interaction_actions.html" '
        'with profile_actions_class=actions_class '
        'profile_dropdown_class=dropdown_class '
        'profile_dropdown_toggle_class=toggle_class '
        'profile_dropdown_menu_class=menu_class '
        'profile_follow_button_extra_class=follow_extra_class '
        'profile_icon_size_class=icon_size_class %}'
    )
    callers = {
        "magazin": {
            "actions": "magazin-profile-actions",
            "dropdown": "magazin-profile-dropdown",
            "toggle": "magazin-profile-dropdown-toggle",
            "menu": "magazin-profile-dropdown-menu",
            "follow_extra": "",
            "icon": "fs-5",
        },
        "studio": {
            "actions": "soho-profile-actions",
            "dropdown": "soho-profile-dropdown",
            "toggle": "soho-profile-dropdown-toggle",
            "menu": "soho-profile-dropdown-menu",
            "follow_extra": "",
            "icon": "fs-5",
        },
        "shared": {
            "actions": "blog-profile-panel__actions",
            "dropdown": "blog-user-dropdown blog-profile-panel__dropdown",
            "toggle": "blog-user-dropdown-toggle blog-profile-panel__dropdown-toggle",
            "menu": "blog-user-dropdown-menu",
            "follow_extra": "blog-profile-panel__follow-btn",
            "icon": "fs-4",
        },
    }

    def render_actions(self, config, user, blog, following=False, restricted=False):
        return self.template.render(
            Context(
                {
                    "request": SimpleNamespace(user=user),
                    "user": user,
                    "blog": blog,
                    "is_following": following,
                    "is_restricted": restricted,
                    "csrf_token": "TOKEN",
                    "actions_class": config["actions"],
                    "dropdown_class": config["dropdown"],
                    "toggle_class": config["toggle"],
                    "menu_class": config["menu"],
                    "follow_extra_class": config["follow_extra"],
                    "icon_size_class": config["icon"],
                }
            )
        )

    def parse(self, html):
        parser = ActionHTMLParser()
        parser.feed(html)
        return parser

    def test_anonymous_and_owner_render_no_actions(self):
        blog = SimpleNamespace(username="author")
        users = (SimpleNamespace(is_authenticated=False), blog)
        for caller, config in self.callers.items():
            for scenario, user in zip(("anonymous", "owner"), users):
                with self.subTest(caller=caller, scenario=scenario):
                    self.assertEqual(self.render_actions(config, user, blog).strip(), "")

    def test_interaction_states_preserve_actions_and_classes(self):
        blog = SimpleNamespace(username="author")
        viewer = SimpleNamespace(is_authenticated=True)
        scenarios = {
            "not_following": (False, False),
            "following": (True, False),
            "restricted": (False, True),
        }
        for caller, config in self.callers.items():
            for scenario, (following, restricted) in scenarios.items():
                with self.subTest(caller=caller, scenario=scenario):
                    parsed = self.parse(
                        self.render_actions(config, viewer, blog, following, restricted)
                    )
                    elements = parsed.elements
                    classes = [attrs.get("class", "") for _, attrs in elements]
                    actions = config["actions"]
                    self.assertIn(actions, classes)
                    self.assertIn(f'dropdown {config["dropdown"]}', classes)
                    self.assertIn(config["toggle"], classes)
                    self.assertIn(f'dropdown-menu dropdown-menu-end {config["menu"]}', classes)
                    self.assertIn(f'bi bi-three-dots {config["icon"]}', classes)

                    forms = [attrs["action"] for tag, attrs in elements if tag == "form"]
                    self.assertIn("/restrict/author/", forms)
                    self.assertIn("/block/author/", forms)
                    if following:
                        self.assertIn("/unfollow/author/", forms)
                        self.assertIn("Pratiš", parsed.text)
                        self.assertIn("Prestani pratiti", parsed.text)
                    else:
                        self.assertIn("/follow/author/", forms)
                        self.assertIn("Prati korisnika", parsed.text)

                    dropdown_follow = [
                        attrs for tag, attrs in elements
                        if tag == "button" and attrs.get("class") == "dropdown-item"
                    ][0]
                    self.assertEqual("disabled" in dropdown_follow, restricted)
                    if restricted:
                        self.assertNotIn("Prati", [text for text in parsed.text if text == "Prati"])
                    else:
                        button_class = next(
                            attrs["class"] for tag, attrs in elements
                            if tag == "button" and attrs.get("class", "").startswith("btn ")
                        )
                        expected_extra = (
                            f' {config["follow_extra"]}' if config["follow_extra"] else ""
                        )
                        expected_state = "btn-outline-primary" if following else "btn-primary"
                        self.assertEqual(
                            button_class,
                            f"btn {expected_state} btn-sm{expected_extra}",
                        )
