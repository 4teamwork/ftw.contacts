from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.contacts.tests import builders
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class ContactsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.contacts:default')
        applyProfile(portal, 'ftw.contacts:simplelayout')
        applyProfile(portal, 'ftw.simplelayout:default')


FTW_CONTACTS_FIXTURE = ContactsLayer()
FTW_CONTACTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_CONTACTS_FIXTURE,),
    name="ftw.contacts:integration")
FTW_CONTACTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_CONTACTS_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.contacts:functional")
