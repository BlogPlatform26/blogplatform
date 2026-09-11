from django.template import Context, Template
from django.test import SimpleTestCase


class SpecialCalendarGridTests(SimpleTestCase):
    template = Template(
        '{% include "blog/components/blog_calendar_grid.html" '
        'with calendar_empty_class=empty_class '
        'calendar_day_class=day_class '
        'calendar_has_post_class=has_post_class '
        'calendar_today_class=today_class %}'
    )
    design_classes = {
        "studio": "soho",
        "magazin": "magazin",
        "nebeska_klasika": "nk",
        "ponocna_elegancija": "pe",
        "ruzicasti_vrt": "rv",
        "stara_aleja": "sa",
        "staza_prema_vrhovima": "spv",
        "jedro_u_suton": "jus",
        "misticno_jezero": "mj",
    }

    def render_case(self, prefix, day, post_days=(), post_map=None, current_day=99):
        return self.template.render(
            Context(
                {
                    "month_calendar": [[day]],
                    "days_with_posts": set(post_days),
                    "day_single_post_map": post_map or {},
                    "current_day": current_day,
                    "archive_base_url": "/blog/audit/",
                    "current_year": 2026,
                    "current_month_num": 9,
                    "empty_class": f"{prefix}-calendar-empty",
                    "day_class": f"{prefix}-calendar-day",
                    "has_post_class": f"{prefix}-calendar-day--has-post",
                    "today_class": f"{prefix}-calendar-day--today",
                }
            )
        )

    def test_all_special_design_calendar_cell_states(self):
        for design, prefix in self.design_classes.items():
            cases = {
                "empty": (0, (), {}, 99, f'<div class="{prefix}-calendar-empty"></div>'),
                "plain": (1, (), {}, 99, f'<div class="{prefix}-calendar-day">1</div>'),
                "today_plain": (2, (), {}, 2, f'<div class="{prefix}-calendar-day {prefix}-calendar-day--today">2</div>'),
                "single": (3, (3,), {3: 123}, 99, f'<a href="/post/123/" class="{prefix}-calendar-day {prefix}-calendar-day--has-post">3</a>'),
                "multiple": (4, (4,), {}, 99, f'<a href="/blog/audit/?year=2026&amp;month=9&amp;day=4" class="{prefix}-calendar-day {prefix}-calendar-day--has-post">4</a>'),
                "today_post": (5, (5,), {5: 123}, 5, f'<a href="/post/123/" class="{prefix}-calendar-day {prefix}-calendar-day--has-post {prefix}-calendar-day--today">5</a>'),
            }
            for state, (day, post_days, post_map, today, expected) in cases.items():
                with self.subTest(design=design, state=state):
                    self.assertHTMLEqual(
                        self.render_case(prefix, day, post_days, post_map, today),
                        expected,
                    )
