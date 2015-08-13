from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.contact import IContact
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from ftw.contacts.testing import FTW_CONTACTS_INTEGRATION_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest2 import TestCase
from zope.component import createObject
from zope.component import queryUtility


class TestDefaultView(TestCase):
    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @browsing
    def test_call_view_does_not_fail(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': '',
            'Firstname': 'Chuck',
            'Lastname': 'N\xc3\xb6rris'}).submit()

        self.assertEqual(1, len(browser.css('#contact-view')))


class TestIdGeneration(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @browsing
    def test_generate_id_from_last_and_firstname(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': '',
            'Firstname': 'Chuck',
            'Lastname': 'N\xc3\xb6rris'}).submit()

        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")

        self.assertEqual(
            "norris-chuck", contactfolder.listFolderContents()[0].id)

    @browsing
    def test_generate_id_from_organization(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': 'CIA Headquarter',
            'Firstname': '',
            'Lastname': ''}).submit()

        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")

        self.assertEqual(
            "cia-headquarter", contactfolder.listFolderContents()[0].id)


class TestTitleGeneration(TestCase):
    """
    """
    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @browsing
    def test_generate_title_from_last_and_firstname(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': '',
            'Firstname': 'Chuck',
            'Lastname': 'N\xc3\xb6rris'}).submit()

        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")

        self.assertEqual(
            u'N\xf6rris Chuck', contactfolder.listFolderContents()[0].title)

    @browsing
    def test_generate_title_from_organization(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': 'CIA Headquarter',
            'Firstname': '',
            'Lastname': ''}).submit()

        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")

        self.assertEqual(
            u"CIA Headquarter", contactfolder.listFolderContents()[0].title)

    @browsing
    def test_setting_title_does_nothing(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': 'CIA Headquarter',
            'Firstname': '',
            'Lastname': ''}).submit()

        contact = contactfolder.listFolderContents()[0]
        contact.setTitle("Chucks Headquarter")

        self.assertEqual(
            u"CIA Headquarter", contactfolder.listFolderContents()[0].title)


class TestContactValidateOrganizationOrFullname(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @browsing
    def test_error_if_no_first_last_and_org_name(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Organization': '',
            'Firstname': '',
            'Lastname': ''}).submit()

        self.assertEqual(1, len(browser.css('.portalMessage.error')))
        self.assertTrue(browser.url.endswith('++add++ftw.contacts.Contact'))

    @browsing
    def test_error_if_only_firstname_exists(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({'Firstname': "Chuck"}).submit()

        self.assertEqual(1, len(browser.css('.portalMessage.error')))
        self.assertTrue(browser.url.endswith('++add++ftw.contacts.Contact'))

    @browsing
    def test_error_if_only_lastname_exists(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({'Lastname': "Norris"}).submit()

        self.assertEqual(1, len(browser.css('.portalMessage.error')))
        self.assertTrue(browser.url.endswith('++add++ftw.contacts.Contact'))

    @browsing
    def test_no_error_if_org_name_exists(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({'Organization': "CIA"}).submit()

        self.assertEqual(0, len(browser.css('.portalMessage.error')))
        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")

    @browsing
    def test_no_error_if_first_and_last_name_exists(self, browser):
        contactfolder = create(
            Builder('contact folder').titled(u'Contact folder'))
        browser.login().visit(
            contactfolder, view="++add++ftw.contacts.Contact")

        browser.fill({
            'Firstname': "Chuck",
            'Lastname': "N\xc3\xb6rris"}).submit()

        self.assertEqual(0, len(browser.css('.portalMessage.error')))
        self.assertEqual(
            1, len(contactfolder.listFolderContents()),
            "Something went wrong while creating the contact")


class TestContactInstallation(TestCase):

    layer = FTW_CONTACTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_adding(self):
        contact = create(Builder('contact'))
        self.assertTrue(IContact.providedBy(contact))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Contact')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Contact')
        schema = fti.lookupSchema()
        self.assertEqual(IContact, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='ftw.contacts.Contact')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IContact.providedBy(new_object))
