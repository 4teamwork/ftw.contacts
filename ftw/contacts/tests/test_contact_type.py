from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.contact import IContact
from ftw.contacts.testing import FTW_CONTACTS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest2 import TestCase
from zope.component import createObject
from zope.component import queryUtility


class TestContactInstallation(TestCase):

    layer = FTW_CONTACTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_adding(self):
        contact = create(
            Builder('contact').titled(u'Chuck Norris'))

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
