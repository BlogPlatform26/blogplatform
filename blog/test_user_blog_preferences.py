from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase

from blog.models import UserBlogPreference
from blog.services import get_blog_preferences, set_blog_preferences


class UserBlogPreferenceServiceTests(TestCase):
    def create_user(self, username, template="magazin"):
        user = User.objects.create_user(username=username, password="test-password")
        user.profile.template = template
        user.profile.save(update_fields=["template"])
        return user

    def test_preferences_are_isolated_for_users_on_same_template(self):
        user_a = self.create_user("preference-user-a")
        user_b = self.create_user("preference-user-b")

        set_blog_preferences(user_a, {
            "posts_per_page": 5,
            "design_customizations": {
                "magazin": {"post_title_color": "#111111"},
            },
        })
        set_blog_preferences(user_b, {
            "posts_per_page": 20,
            "design_customizations": {
                "magazin": {"post_title_color": "#eeeeee"},
            },
        })

        prefs_a = get_blog_preferences(user_a)
        prefs_b = get_blog_preferences(user_b)

        self.assertEqual(prefs_a["posts_per_page"], 5)
        self.assertEqual(prefs_b["posts_per_page"], 20)
        self.assertEqual(
            prefs_a["design_customizations"]["magazin"]["post_title_color"],
            "#111111",
        )
        self.assertEqual(
            prefs_b["design_customizations"]["magazin"]["post_title_color"],
            "#eeeeee",
        )
        self.assertEqual(UserBlogPreference.objects.count(), 2)

    def test_updating_one_user_does_not_touch_the_other_user(self):
        user_a = self.create_user("preference-update-a")
        user_b = self.create_user("preference-update-b")
        set_blog_preferences(user_a, {"posts_per_page": 5})
        set_blog_preferences(user_b, {"posts_per_page": 20})

        preference_b = UserBlogPreference.objects.get(user=user_b)
        original_data = preference_b.data.copy()
        original_updated_at = preference_b.updated_at

        set_blog_preferences(user_a, {"posts_per_page": 10})

        preference_b.refresh_from_db()
        self.assertEqual(preference_b.data, original_data)
        self.assertEqual(preference_b.updated_at, original_updated_at)

    def test_one_user_keeps_customizations_for_multiple_templates(self):
        user = self.create_user("preference-multiple-designs", template="default")
        set_blog_preferences(user, {
            "design_customizations": {
                "default": {"post_title_color": "#123456"},
                "magazin": {"post_title_color": "#abcdef"},
            },
        })

        default_prefs = get_blog_preferences(user)
        self.assertEqual(
            default_prefs["active_design_customization"]["post_title_color"],
            "#123456",
        )

        user.profile.template = "magazin"
        user.profile.save(update_fields=["template"])
        magazin_prefs = get_blog_preferences(user)

        self.assertEqual(
            magazin_prefs["active_design_customization"]["post_title_color"],
            "#abcdef",
        )
        self.assertEqual(
            magazin_prefs["design_customizations"]["default"]["post_title_color"],
            "#123456",
        )

    def test_string_template_key_is_rejected(self):
        with self.assertRaises(TypeError):
            get_blog_preferences("magazin")
        with self.assertRaises(TypeError):
            set_blog_preferences("magazin", {})

    def test_deleting_user_cascades_only_its_preferences(self):
        user_a = self.create_user("preference-delete-a")
        user_b = self.create_user("preference-delete-b")
        set_blog_preferences(user_a, {"posts_per_page": 5})
        set_blog_preferences(user_b, {"posts_per_page": 20})

        user_a_id = user_a.pk
        user_a.delete()

        self.assertFalse(UserBlogPreference.objects.filter(user_id=user_a_id).exists())
        self.assertTrue(UserBlogPreference.objects.filter(user=user_b).exists())


class UserBlogPreferenceMigrationTests(TransactionTestCase):
    migrate_from = [("blog", "0075_alter_comment_options_and_more")]
    migrate_to = [("blog", "0076_user_blog_preference")]

    def setUp(self):
        super().setUp()
        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_from)
        old_apps = self.executor.loader.project_state(self.migrate_from).apps

        UserModel = old_apps.get_model("auth", "User")
        LegacyPreference = old_apps.get_model("blog", "BlogDesignPreference")

        self.migrated_user = UserModel.objects.create(
            id=101,
            username="migration-existing-user",
        )
        self.second_user = UserModel.objects.create(
            id=102,
            username="migration-second-user",
        )
        self.expected_data = {
            "posts_per_page": 15,
            "design_customizations": {
                "default": {"post_title_color": "#101010"},
                "magazin": {"post_title_color": "#202020"},
            },
        }
        LegacyPreference.objects.create(template="101", data=self.expected_data)
        LegacyPreference.objects.create(
            template="999999",
            data={"posts_per_page": 20},
        )
        LegacyPreference.objects.create(
            template="magazin",
            data={"posts_per_page": 5},
        )

        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_to)
        self.apps = self.executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_only_numeric_legacy_record_with_existing_user_is_backfilled(self):
        NewPreference = self.apps.get_model("blog", "UserBlogPreference")
        LegacyPreference = self.apps.get_model("blog", "BlogDesignPreference")

        migrated = NewPreference.objects.get(user_id=101)
        self.assertEqual(migrated.data, self.expected_data)
        self.assertFalse(NewPreference.objects.filter(user_id=102).exists())
        self.assertEqual(NewPreference.objects.count(), 1)

        self.assertTrue(LegacyPreference.objects.filter(template="101").exists())
        self.assertTrue(LegacyPreference.objects.filter(template="999999").exists())
        self.assertTrue(LegacyPreference.objects.filter(template="magazin").exists())
