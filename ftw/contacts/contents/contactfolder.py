from ftw.contacts.interfaces import IContactFolder
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements


class IContactFolderSchema(model.Schema):
    """A contactfolder type schema interface
    """


class ContactFolder(Container):
    """A contactfolder
    """
    implements(IContactFolder)
