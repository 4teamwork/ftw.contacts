from collective.geo.settings.interfaces import IGeoSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def georef_settings(context):
    """Import step to set up Contact as georeferenceable type in
    collective.geo.settings.

    This just adds a registry entry, but it can't be done through registry.xml
    because at that point the Contact type hasn't been registered yet.
    """
    registry = getUtility(IRegistry)
    geo_content_types = registry.forInterface(IGeoSettings).geo_content_types
    if 'ftw.contacts.Contcat' not in geo_content_types:
        geo_content_types.append('ftw.contacts.Contact')


def import_various(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile(
            'ftw.contacts_various.txt') is None:
        return

    site = context.getSite()
    georef_settings(site)
