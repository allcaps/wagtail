import shutil
import tempfile

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

TMP_ROOT = tempfile.mkdtemp()

USERNAME = "john"
PASSWORD = get_user_model().objects.make_random_password()


def pytest_configure():
    from django.conf import settings

    settings.DEBUG = True
    settings.STATIC_ROOT = f"{TMP_ROOT}/static/"
    settings.MEDIA_ROOT = f"{TMP_ROOT}/media/"
    settings.DOCUMENT_ROOT = f"{TMP_ROOT}/docs/"

    from django.core.management import call_command
    call_command("collectstatic")


def pytest_unconfigure():
    shutil.rmtree(TMP_ROOT, ignore_errors=True)


@pytest.fixture
def base_user(db):
    user = get_user_model().objects.create(
        username=USERNAME,
        is_active=True,
        is_staff=True,
        email="john@example.com",
    )
    user.set_password(PASSWORD)
    return user


@pytest.fixture
def superuser(db, base_user):
    base_user.is_superuser = True
    base_user.save()
    return base_user


@pytest.fixture
def superuser_client(client, superuser):
    client.force_login(superuser, backend=None)
    return client


@pytest.fixture
def authenticated_client(client, base_user):
    client.force_login(base_user, backend=None)
    return client


class DriverWithShortcuts(webdriver.Chrome):
    def click_link(self, link_text):
        self.find_element_by_link_text(link_text).click()

    def click_button(self, button_text):
        self.find_element_by_xpath(f"//button[text()='{button_text}']").click()

    def input_text(self, field_name, text):
        self.find_element_by_name(field_name).send_keys(text)

    def update_input_text(self, field_name, text):
        self.find_element_by_name(field_name).clear()
        self.find_element_by_name(field_name).send_keys(text)

    def scroll_to_bottom(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")


@pytest.fixture()
def driver():
    """Provide a selenium webdriver instance"""
    options = webdriver.ChromeOptions()

    if settings.SELENIUM_HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model
    driver = DriverWithShortcuts(
        # command_executor=settings.SELENIUM_REMOTE_URL,
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    driver.set_window_size(1024, 768)
    yield driver
    # Tear down
    driver.quit()


@pytest.fixture()
def unauthenticated_driver(driver, live_server):
    """Return a browser instance with logged-in user session"""
    driver.get(live_server.url)
    driver.refresh()
    return driver


@pytest.fixture()
def authenticated_driver(driver, authenticated_client, live_server):
    """Return a browser instance with logged-in user session"""
    driver.get(live_server.url)
    cookie = authenticated_client.cookies["sessionid"]
    driver.add_cookie(
        {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
    )
    driver.refresh()
    return driver


@pytest.fixture()
def superuser_driver(driver, superuser_client, live_server):
    """Return a browser instance with logged-in superuser session"""
    driver.get(live_server.url)
    cookie = superuser_client.cookies["sessionid"]
    driver.add_cookie(
        {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
    )
    driver.refresh()

    return driver
