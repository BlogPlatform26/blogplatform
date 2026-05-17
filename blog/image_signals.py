from django.db.models.signals import post_save
from django.dispatch import receiver

from .image_utils import optimize_blog_banner_field, optimize_image_field
from .models import (
    CategoryHomeImage,
    Post,
    PostImage,
    Profile,
    SiteMessage,
)


@receiver(post_save, sender=Post)
def optimize_post_image(sender, instance, **kwargs):
    optimize_image_field(instance, "image")


@receiver(post_save, sender=PostImage)
def optimize_post_extra_image(sender, instance, **kwargs):
    optimize_image_field(instance, "image")


@receiver(post_save, sender=Profile)
def optimize_profile_images(sender, instance, **kwargs):
    optimize_image_field(instance, "avatar", max_width=900, max_height=900, quality=95)
    optimize_blog_banner_field(instance, "blog_banner")
    optimize_image_field(instance, "simple_background_image")
    optimize_image_field(instance, "soho_hero_image")


@receiver(post_save, sender=CategoryHomeImage)
def optimize_category_home_image(sender, instance, **kwargs):
    optimize_image_field(instance, "image")


@receiver(post_save, sender=SiteMessage)
def optimize_site_message_image(sender, instance, **kwargs):
    optimize_image_field(instance, "image")
