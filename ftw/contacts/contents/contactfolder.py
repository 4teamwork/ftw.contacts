from plone.dexterity.content import Container
from plone.supermodel import model


class IContactFolder(model.Schema):
    """A contactfolder type schema interface
    """


class ContactFolder(Container):
    """A contactfolder
    """
