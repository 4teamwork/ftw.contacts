from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.api.content import delete
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase

import transaction


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

        member_block = create(Builder('member block')
                              .within(self.contactfolder)
                              .contact(contact)
                              .titled(u"A MemberBlock")
                              .having(show_title=True))

        browser.login().visit(member_block, view="block_view")
        self.assertEqual(u'A MemberBlock', browser.css('h3').first.text)

    @browsing
    def test_call_with_deleted_contact_returns_hint(self, browser):

        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member_block = create(Builder('member block')
                              .within(self.contactfolder)
                              .contact(contact))

        delete(contact)
        transaction.commit()

        browser.login().visit(member_block, view="block_view")

        self.assertEqual(1, len(browser.css('#member-no-contact-exist')))

    @browsing
    def test_call_returns_member_view(self, browser):
        contact = create(Builder('contact')
                         .with_maximal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member_block = create(Builder('member block')
                              .within(self.contactfolder)
                              .contact(contact))

        browser.login().visit(member_block, view="block_view")

        self.assertEqual(0, len(browser.css('#member-no-contact-exist')))
        self.assertEqual(0, len(browser.css('#member-empty')))
        self.assertEqual(1, len(browser.css('.memberContactInfo')))

    @browsing
    def test_anonymous_without_contact_returns_no_content(self, browser):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member_block = create(Builder('member block')
                              .within(self.contactfolder)
                              .contact(contact))

        delete(contact)
        transaction.commit()

        browser.visit(member_block, view="block_view")

        self.assertEqual(1, len(browser.css('#member-empty')))
