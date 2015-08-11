from plone.dexterity.content import Item
from plone.supermodel import model


class IContact(model.Schema):
    """A contact type schema interface
    """


class Contact(Item):
    """A contact
    """
