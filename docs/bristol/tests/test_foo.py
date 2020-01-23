from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.keys import Keys

from .documentation_factory import DocumentationFactory

# https://github.com/gsnedders/wcag-contrast-ratio
import wcag_contrast_ratio as contrast


def convert_rgb_range(val):
    """
    convert_rgb_range, from Selenium RGBA 255 (string) to wcag_contrast_ratio (list of floats).

    - Quick and dirty
    - Ignore alpha
    - Convert 255 to 1 based

    :param val: "rgba(255, 255, 255, 1)" (string)
    :return: [1,1,1] (list of floats)
    """
    val = val.replace("rgba(", "").replace(")", "").replace(",", "")
    rgb_256 = list([int(s) for s in val.split() if s.isdigit()])[:-1]
    return [1.0 / 255 * val for val in rgb_256]


def test_wagtail(unauthenticated_driver, live_server):
    driver = unauthenticated_driver
    base_url = live_server.url
    driver.get(base_url)

    with DocumentationFactory(
        "demo.rst", "Homepage", driver
    ) as doc:
        doc.p("This is an example of how to interact with Selenium Driver and create an user-guide.")
        doc.p(
            "Given:\n\n"
            "- A new Wagtail project. Created with ``wagtail start bristol``.\n"
            "- No session. The user is logged out.\n"
        )

        doc.h2("Homepage")
        doc.p("Wagtail comes without a frontend. The default homepage displays a hatching egg and some hints.")
        doc.img("home.png")

        doc.h2("Login")
        wagtail_index_url = base_url + reverse("wagtailadmin_home")
        doc.p(f"Let's open the Wagtail admin at {wagtail_index_url}.")
        driver.get(live_server.url + "/admin/")
        doc.p(f"There was a redirect from {wagtail_index_url} to {driver.current_url}. We need to login first.")

        # - Create content
        username, password = "jane", "secret_password"
        get_user_model().objects.create_superuser(
            username=username,
            password=password,
            is_active=True,
            email=f"{username}@example.com",
        )
        # - Assert backend obj exists
        assert get_user_model().objects.count() == 1

        driver.input_text("username", username)
        driver.input_text("password", password)
        doc.img("login_button.png", driver.find_element_by_xpath(f"//button"))
        driver.find_element_by_xpath(f"//button").click()

        doc.p(f"This is the Wagtail admin homepage.")
        doc.img("index.png")

        doc.h2("Color contrast")
        doc.p("Inspect the search input and assert sufficient color contrast.")
        element = driver.find_element_by_id("menu-search-q")
        color = element.value_of_css_property("color")
        background_color = element.value_of_css_property("background-color")

        color = convert_rgb_range(color)
        background_color = convert_rgb_range(background_color)
        ratio = contrast.rgb(background_color, color)

        assert contrast.passes_AA(ratio)
        doc.p(
            f"The search box text vs background contrast ratio is {ratio}. "
            f"AA {contrast.passes_AA(ratio)} AAA {contrast.passes_AAA(ratio)}"
        )
        doc.img("search.png", element)

        doc.h2("Tab index")
        doc.p("Let's press tab until the focus is back on the first element.")

        elements = []
        first_element = driver.find_element_by_tag_name('body').send_keys(Keys.TAB)

        breakpoint()
        doc.img("tab.png", element)
        print("aie!")




        # Count how many elements with the tabindex attribute exist on the page -
        # this is to handle any divs that have been made clickable with a specific tab index
        counterTabIndex = len(driver.find_elements_by_xpath("//*[@tabindex]"))
        #
        # # Count how many a link elements exist on the page
        # countAnchor = len(driver.find_elements_by_xpath("//a"))
        #
        # # Print tabindex element count number to console
        # print
        # counterTabIndex, 'elements with a tabindex found on this page'
        #
        # # Print a link count number to console
        # print
        # countAnchor, 'ahref elements found on this page'
        #
        # # Add them together for the total count
        # totalCounter = counterTabIndex + countAnchor
        #
        # # Loop and tab through all elements. Note the length of the loop is defined by the element count done above
        # for x in range(0, totalCounter):
        #     time.sleep(0.2)
        #     driver.switch_to_active_element().send_keys(Keys.TAB)
