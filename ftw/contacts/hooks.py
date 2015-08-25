from collective.geo.settings.interfaces import IGeoSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def default_profile_installed(site):
    georef_settings(site)


def georef_settings(context):
    """Import step to set up Contact as georeferenceable type in
    collective.geo.settings.

    This just adds a registry entry, but it can't be done through registry.xml
    because at that point the Contact type hasn't been registered yet.
    """
    registry = getUtility(IRegistry)
    geo_content_types = registry.forInterface(IGeoSettings).geo_content_types
    if 'ftw.contacts.Contact' not in geo_content_types:
        geo_content_types.append('ftw.contacts.Contact')
