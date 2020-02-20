Introduction
============

This package provides a contact contenttype.

.. contents:: Table of Contents


Installation
------------

Add the package as dependency to your setup.py:

.. code:: python

  setup(...
        install_requires=[
          'ftw.contacts',
        ])

or to your buildout configuration:

.. code:: ini

  [instance]
  eggs += ftw.contacts

and rerun buildout.

For Plone 4.x add `eggs += ftw.contacts ['plone4']` option.

Install the Generic Setup profile.


Functionality Overview
----------------------

- Contact directory with ajax search functionality
- Contact content type
- KML-Representation of Contact
- vCard-Representation of Contact
- `ftw.zipexport`_ integration if you install the [zipexport] extra
- `ftw.simplelayout`_ integration if you install the [simplelayout] extra
- Synchronization of contacts with an LDAP service.

How it looks
------------

The ``ftw.contacts`` package provides an intuitive contact directory...

.. image:: https://raw.github.com/4teamwork/ftw.contacts/master/docs/images/contactdirectory.png

... with a detailed contact-view.

.. image:: https://raw.github.com/4teamwork/ftw.contacts/master/docs/images/contact.png

How it works
------------

Contactfolder
~~~~~~~~~~~~~

This is a dexterity contenttype and acts as a container for contacts to be listed.

After installing the ``ftw.contacts`` package you can add a ``Contactfolder`` to your Plone site.

The ``Contactfolder`` provides an intuitive overview of all available contacts.
By default, the first 20 contacts will be shown and you can load more contacts by clicking on the
``Load more`` button at the end of the list.

The alphabetical filter allows the user to quickly find a contact. Furthermore contacts can be found by using the search field.

All the requests are asynchronous and work with a large number of contacts.

Contact
~~~~~~~

This is a dexterity contenttype which can be added inside a ``Contactfolder``.

A ``Contact`` lists all available attributes on the contact.

You have also the possibility to show the contacts location on a map.

In addition you can download the KML-representation or the vCard-representation of the contact.

ftw.simplelayout integration
----------------------------

This is an addon for `ftw.simplelayout`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

Add the simplelayout extra to your egg:

.. code:: ini

  [instance]
  eggs += ftw.contacts [simplelayout]

Run buildout and install the ``ftw.contacts.simplelayout:default`` profile

You'll get a new contenttype ``MemberBlock`` which is available in a contentpage.

If you don't know `ftw.simplelayout`_, please read https://github.com/4teamwork/ftw.simplelayout

MemberBlock
~~~~~~~~~~~

The memberblock connects the a Contact with a simplelayout page.
You just have to define the Contact attributes once and you can reuse them through
the memberblock.


ftw.geo integration
-------------------

Add the geo extra to your egg:

.. code:: ini

  [instance]
  eggs += ftw.contacts [geo]

Run buildout and install the ``ftw.contacts.geo:default`` profile

After installing the geo-extra, you'll see a map layer on each contact-type
if you entered a valid address.

If you don't know `ftw.geo`_, please read https://github.com/4teamwork/ftw.geo

Contact synchronization through LDAP
------------------------------------

The synchronization is executed through the ``sync_contacts`` entry point. The configuration
for the sync is as follows:

- The Plone site on which to execute the sync: Parameter ``-p`` - only required when there are multiple sites.
- The path to the contacts folder: Configured in the registry under ``IContactsSettings.contacts_path``
- The mapping of the LDAP attributes to the contact fields and which field to use as ID: Register a ``ILDAPAttributeMapper`` utility. Default: ``DefaultLDAPAttributeMapper``

- The LDAP plugin id inside of ``acl_users``: Configured in the registry under ``IContactsSettings.ldap_plugin_id``
- The base DN for the contacts. Parameter ``-b`` - defaults to the base DN configured in the plugin
- The filter LDAP query to only get contacts. Parameter ``-f`` - defaults to ``(objectClass=*)``

Synchronize contacts from multiple ldap sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To synchronize multiple sources (multiple plugins in ``acl_users``) a config file is required.
Pass the path to the file through the ``-c`` parameter.

The only required attribute per source is the ``ldap_plugin_id`. ``base_dn`` will default to the base DN of the plugin and ``filter`` will default to ``(objectClass=*)``.

To avoid id collisions a ``userid_prefix`` can be specified. The prefix will then be applied to all contacts of this source.
When an existing site wants to add a second source but already has synchronized contacts, then you should only
specify a prefix for the new source.  With this method the id's of the existing source do not change and contacts
that have already been synchronized can still be identified.
This is important, because the customer may have already added additional information (e.g. images) to the contacts.
If the ids change the sync will not recognize them and would then delete them!

Scope can be set to: ``SCOPE_BASE``, ``SCOPE_ONELEVEL``, ``SCOPE_SUBTREE`` or ``SCOPE_SUBORDINATE``.

.. code:: json

    [
        {
            "ldap_plugin_id": "intern",
            "base_dn": "ou=Employees,ou=Users,dc=4teamwork,dc=ch",
            "filter": "(objectClass=*)"
        },
        {
            "ldap_plugin_id": "extern",
            "userid_prefix": "extern-",
            "base_dn": "ou=Customers,ou=Users,dc=4teamwork,dc=ch",
            "filter": "(objectClass=*)",
            "scope": "SCOPE_ONELEVEL"
        }
    ]

Compatibility
-------------

Plone 4.3 and 5.1

.. image:: https://jenkins.4teamwork.ch/job/ftw.contacts-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.contacts-master-test-plone-4.3.x.cfg


Links
-----

- Github: https://github.com/4teamwork/ftw.contacts
- Issues: https://github.com/4teamwork/ftw.contacts/issues
- Pypi: http://pypi.python.org/pypi/ftw.contacts
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.contacts


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contacts`` is licensed under GNU General Public License, version 2.

.. _ftw.zipexport: https://github.com/4teamwork/ftw.zipexport
.. _ftw.simplelayout: https://github.com/4teamwork/ftw.simplelayout
.. _ftw.geo: https://github.com/4teamwork/ftw.geo
