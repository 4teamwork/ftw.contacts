from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase


class TestMemberBlockView(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))

    @browsing
    def test_call_view_does_not_fail(self, browser):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .titled(u"A Member")
                        .having(show_title=True))

        browser.login().visit(member, view="block_view")
        self.assertEqual(u'A Member', browser.css('h3').first.text)

    @browsing
    def test_image_caption_is_contact_title_if_has_permission(self, browser):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .titled(u"A Member")
                        .having(show_image=True))

        browser.login().visit(member, view="block_view")

        self.assertEqual(
            u'Ch\xf6ck 4orris',
            browser.css('.imageCaption').first.text)
