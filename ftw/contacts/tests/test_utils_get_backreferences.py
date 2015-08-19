from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.member import IMember
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from ftw.contacts.utils import get_backreferences
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase


class TestBackReferences(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))

    def test_references_in_a_list(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes"))

        self.assertEqual(
            [member], get_backreferences(contact, IMember))

    def test_empty_list_if_no_references_found(self):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        self.assertEqual([], get_backreferences(contact, IMember))
