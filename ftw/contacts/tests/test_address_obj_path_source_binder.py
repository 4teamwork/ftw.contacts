from ftw.contacts.simplelayout.contents.memberblock import AddressObjPathSourceBinder
from ftw.contacts.simplelayout.interfaces import IMemberRegistry
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from plone.registry.interfaces import IRegistry
from unittest2 import TestCase
from zope.component import getUtility


class TestAddressObjPathSourceBinder(TestCase):

    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_nav_tree_query_is_plone_root_by_default(self):
        AddressObjPathSourceBinder()
        sourcebinder = AddressObjPathSourceBinder()(self.portal)

        self.assertEqual(
            {'query': '/plone'},
            sourcebinder.navigation_tree_query.get('path')
        )

    def test_change_nav_tree_query_path_in_registry(self):
        registry = getUtility(IRegistry).forInterface(IMemberRegistry)
        registry.member_nav_tree_query_path = u"/address"

        AddressObjPathSourceBinder()
        sourcebinder = AddressObjPathSourceBinder()(self.portal)

        self.assertEqual(
            {'query': '/plone/address'},
            sourcebinder.navigation_tree_query.get('path')
        )
