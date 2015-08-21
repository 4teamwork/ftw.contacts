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

Install the Generic Setup profile.

Motivation
----------

The ``ftw.contacts`` modernize the very old egov.contactdirectory and
prepares the package for plone 5 integration.

Quick overview of the functions
-------------------------------

- Contactdirectory with ajax search functionality
- Contact
- KML-Representation of Contact
- vCard-Representation of Contact
- ftw.zipexport integration if you install the [zipexport]-extra
- ftw.simplelayout integration if you install the [simplelayout]-extra

How it looks
------------

The ``ftw.contacts`package provides a nice contactdirectory.

.. image:: https://raw.github.com/4teamwork/ftw.contacts/master/docs/contactdirectory.png

with a contact-view.

.. image:: https://raw.github.com/4teamwork/ftw.contacts/master/docs/contact.png

How it works
------------

Contactfolder
~~~~~~~~~~~~~

After installing the ``ftw.contacts`` package you can add a ``Contactfolder``to your plonesite.

The ``Contactfolder``provides a nice overview of all avaiable contacts.
Per default, the first 20 contacts will be shown and you can load more contacts by clicking on the
``Load more``butten at the end of the list.

You can search for contacts by filtering them trought the letters listed above the listing.
Otherwise you can search contact by type in something into the search field.

All the requests are asynchron and works also with a big amount of contacts

Contact
~~~~~~~

The ``contact`` lists all attributes on the available on the contact.

You have also the possiblity to show the contacts location on a map.

In addition you can download the kml-representation or the vCard-representation of the contact.

ftw.simplelayout integration
----------------------------

Add the simplelayout extra to your egg:

.. code:: ini

  [instance]
  eggs += ftw.contacts [simplelayout]

Run buildout and install the ``ftw.contacts: simplelayout``profile

You'll get a new contenttype ``MemberBlock`` which is available in a contentpage.

If you don't know ftw.simplelayout, please read https://github.com/4teamwork/ftw.simplelayout

MemberBlock
~~~~~~~~~~~

The memberblock connects the a Contact with a simplelayout page.
You just have do define the Contact attributes once an you can reuse them trough
the memberblock


Compatibility
-------------

Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.lawgiver-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.lawgiver-master-test-plone-4.3.x.cfg


Links
-----

- Github: https://github.com/4teamwork/ftw.contacts
- Issues: https://github.com/4teamwork/ftw.contacts/issues
- Pypi: http://pypi.python.org/pypi/ftw.contacts
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.contacts


Copyright
----------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contacts`` is licensed under GNU General Public License, version 2.
