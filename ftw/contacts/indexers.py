from ftw.contacts.interfaces import IContact
from plone.indexer.decorator import indexer


@indexer(IContact)
def getIcon(obj):
    # Always return False with Plone 5. We never want a Icon here.
    return False
