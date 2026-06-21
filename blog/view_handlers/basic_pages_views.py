from django.shortcuts import render


def terms_of_use(request):
    return render(request, "blog/basic_pages/terms_of_use.html")


from django.shortcuts import render


def terms_of_use(request):
    return render(request, "blog/basic_pages/terms_of_use.html")


def privacy_policy(request):
    return render(request, "blog/basic_pages/privacy_policy.html")


from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def terms_of_use(request):
    return render(request, "blog/basic_pages/terms_of_use.html")


def privacy_policy(request):
    return render(request, "blog/basic_pages/privacy_policy.html")


def content_rules(request):
    return render(request, "blog/basic_pages/content_rules.html")


def sitemap_xml(request):
    urls = [
        request.build_absolute_uri(reverse("home")),
        request.build_absolute_uri(reverse("terms_of_use")),
        request.build_absolute_uri(reverse("privacy_policy")),
        request.build_absolute_uri(reverse("content_rules")),
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{url}</loc>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return HttpResponse("\n".join(xml), content_type="application/xml")

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap_xml'))}",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")

def google_site_verification(request):
    return HttpResponse(
        "google-site-verification: google971f18637c646cba.html",
        content_type="text/plain"
    )