import unittest

from django.test import override_settings

from wagtail.core.models import Locale, Page
from wagtail.core.tests.test_locale_model import make_test_page
from wagtail.tests.utils import WagtailTestUtils


@override_settings(
    LANGUAGES=[
        ("en", "English"),
        ("fr", "French"),
        ("de", "German"),
        ("es", "Spanish"),
    ],
    WAGTAIL_CONTENT_LANGUAGES=[
        ("en", "English"),
        ("fr", "French"),
        ("de", "German"),
        ("es", "Spanish"),
    ],
)
class TestSubmitPageTranslation(unittest.TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        self.en_locale = Locale.objects.get()
        self.fr_locale = Locale.objects.create(language_code="fr")
        self.de_locale = Locale.objects.create(language_code="de")

        self.en_homepage = Page.objects.get(depth=2)
        self.fr_homepage = self.en_homepage.copy_for_translation(self.fr_locale)
        self.de_homepage = self.en_homepage.copy_for_translation(self.de_locale)

        self.en_blog_index = make_test_page(self.en_homepage, title="Blog", slug="blog")
        self.en_blog_post = make_test_page(
            self.en_blog_index, title="Blog post", slug="blog-post"
        )
        self.en_blog_post_child = make_test_page(
            self.en_blog_post, title="A deep page", slug="deep-page"
        )
