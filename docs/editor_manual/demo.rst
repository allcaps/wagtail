Homepage
========

This is an example of how to interact with Selenium Driver and create an user-guide.

Given:

- A new Wagtail project. Created with ``wagtail start bristol``.
- No session. The user is logged out.


Homepage
--------

Wagtail comes without a frontend. The default homepage displays a hatching egg and some hints.

.. image:: /_static/images/home.png

Login
-----

Let's open the Wagtail admin at http://10.10.10.238:8000/admin/.

There was a redirect from http://10.10.10.238:8000/admin/ to http://10.10.10.238:8000/admin/login/?next=/admin/. We need to login first.

.. image:: /_static/images/login_button.png

This is the Wagtail admin homepage.

.. image:: /_static/images/index.png

Color contrast
--------------

Inspect the search input and assert sufficient color contrast.

The search box text vs backgound contrast ratio is 7.867507073708571. AA True AAA True

.. image:: /_static/images/search.png

Tab index
---------

Let's press tab untill the focus is back on the first element.

.. image:: /_static/images/tab.png