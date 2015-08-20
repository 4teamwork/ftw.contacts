from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.member import IMember
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.api.content import delete
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest2 import TestCase
from zope.component import createObject
from zope.component import queryUtility
import transaction


class TestDefaultView(TestCase):
    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))

    @browsing
    def test_call_with_deleted_contact_returns_hint(self, browser):

        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes"))

        delete(contact)
        transaction.commit()

        browser.login().visit(member)

        self.assertEqual(1, len(browser.css('#member-no-contact-exist')))

    @browsing
    def test_call_returns_member_view(self, browser):
        contact = create(Builder('contact')
                         .with_maximal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes"))

        browser.login().visit(member)

        self.assertEqual(1, len(browser.css('#member-view')))

    @browsing
    def test_anonymous_without_contact_returns_no_content(self, browser):
        contact = create(Builder('contact')
                         .with_minimal_info(u'Ch\xf6ck', u'4orris')
                         .within(self.contactfolder))

        member = create(Builder('member')
                        .within(self.contactfolder)
                        .contact(contact)
                        .having(
                            firstname=u"J\xf6mes"))

        delete(contact)
        transaction.commit()

        browser.visit(member)

        self.assertEqual(1, len(browser.css('#member-empty')))


class TestMemberInstallation(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_adding(self):
        member = create(Builder('member'))
        self.assertTrue(IMember.providedBy(member))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Member')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Member')
        schema = fti.lookupSchema()
        self.assertEqual(IMember, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Member')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IMember.providedBy(new_object))
