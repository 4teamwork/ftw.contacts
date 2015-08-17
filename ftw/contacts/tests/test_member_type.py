from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.member import IMember
from ftw.contacts.testing import FTW_CONTACTS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest2 import TestCase
from zope.component import createObject
from zope.component import queryUtility


class TestMemberInstallation(TestCase):

    layer = FTW_CONTACTS_INTEGRATION_TESTING

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
