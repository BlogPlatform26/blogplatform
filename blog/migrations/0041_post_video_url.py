from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0040_comment_is_anonymous_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="video_url",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]