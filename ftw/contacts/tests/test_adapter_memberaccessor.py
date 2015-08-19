from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.interfaces import IMemberAccessor
from ftw.contacts.testing import FTW_CONTACTS_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class TestMemberAccessor(TestCase):

    layer = FTW_CONTACTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))

    def test_get_attr_on_member_if_not_aquire_address(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Chuck', u'4\xf6rris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes"))

        self.assertEqual(u'J\xf6mes', IMemberAccessor(member).firstname)

    def test_get_attr_on_contact_if_aquire_address(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes",
                            acquire_address=True))

        self.assertEqual(u'Ch\xf6ck', IMemberAccessor(member).firstname)

    def test_get_attr_on_member_if_aquire_address_but_attr_not_exist(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Chuck', u'4\xf6rris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            acquire_address=True,
                            show_title=True))

        self.assertEqual(False, hasattr(contact, 'show_title'))
        self.assertEqual(True, IMemberAccessor(member).show_title)

    def test_get_not_existing_attr_returns_none(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Chuck', u'4\xf6rris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact))

        self.assertEqual(None, IMemberAccessor(member).not_existing_attr)