.. _icons:

=====
Icons
=====

Wagtail comes with an icon set.
The icons are used throughout the admin interface.

Elements that use icons are:

- :ref:`Various menu items <admin_hooks>`
- :ref:`ModelAdmin menu items <modeladmin_menu_icon>`
- :ref:`Streamfield blocks <basic_block_type_icon>`
- :ref:`Rich text editor toolbar buttons <extending_the_draftail_editor>`
- ...

This document describes how to choose and add icons.

Available icons and their names
-------------------------------

Enable the :ref:`styleguide <styleguide>` to view icons and their names.

Alternatively inspect the source code ``wagtail/admin/wagtail_hooks.py``.
The filename without ``.svg`` is the icon name.

Add a custom icon
-----------------

Draw or download an icon.

The SVG should:

 - Have a size of 16x16 points
 - Contain a ``symbol`` tag
 - Have ``id="icon-<name>"`` attribute
 - Not set the ``fill`` attribute
 - Not set the ``xmlns`` attribute

This SVG:

.. code-block:: html

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
      <path fill="black" d="M0 0h16v16H0z"/>
    </svg>


Converted to a SVG symbol:

.. code-block:: html

    <symbol id="icon-square" viewBox="0 0 16 16">
        <path d="M0 0h16v16H0z"/>
    </symbol>


Add the icon to the set with the ``register_icons`` hook.

.. code-block:: python

    @hooks.register("register_icons")
    def register_icons(icons):
        return icons + ['path/to/rocket.svg']


Changing icons via template override
------------------------------------

When several applications provide different versions of the same template,
the application listed first in ``INSTALLED_APPS`` has precedence.

Place your app before any Wagtail apps in ``INSTALLED_APPS``.

Wagtail icons live in ``wagtail/admin/templates/wagtailadmin/icons/``.
Place your own SVG files in ``<your_app>/templates/wagtailadmin/icons/``.

Changing icons via hooks
------------------------

.. code-block:: python

    @hooks.register("register_icons")
    def register_icons(icons):
        icons.remove("wagtailadmin/icons/time.svg")  # Remove the original icon
        icons.append("path/to/time.svg")  # Add the new icon
        return icons

Icon template tag
-----------------

Use an icon in a custom template:

.. code-block:: html+django

    {% load wagtailadmin_tags %}
    {% icon name="rocket" classname="..." title="Launch" %}


Icon font support
-----------------

Use the ``insert_global_admin_css`` and reference your icons via ``class_names``.