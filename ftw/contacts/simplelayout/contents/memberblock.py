from collective import dexteritytextindexer
from ftw.contacts import _
from ftw.contacts.interfaces import IContact
from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.simplelayout.interfaces import IMemberRegistry
from ftw.contacts.utils import get_organization
from plone import api
from plone.dexterity.content import Item
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.schema.email import RFC822MailAddress
from zope import schema
from zope.component import getUtility
from zope.interface import implements


class AddressObjPathSourceBinder(ObjPathSourceBinder):
    def __init__(self):
        super(AddressObjPathSourceBinder, self).__init__(
            navigation_tree_query={},
            object_provides=IContact.__identifier__)

    def __call__(self, context):
        portal = api.portal.get()
        portal_path = '/'.join(portal.getPhysicalPath())

        registry = getUtility(IRegistry).forInterface(IMemberRegistry)
        path = registry.member_nav_tree_query_path or ''

        self.navigation_tree_query['path'] = {
            'query': portal_path + path}

        return super(AddressObjPathSourceBinder, self).__call__(context)


class IMemberBlockSchema(model.Schema):
    """A member type schema interface
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        missing_value=u"",
        default=u"",
        required=False)

    show_title = schema.Bool(
        title=_(u'label_show_title', default=u'Show title'),
        required=False)

    contact = RelationChoice(
        title=_(u'label_contact_reference', default=u'Contact reference'),
        source=AddressObjPathSourceBinder(),
        required=True)

    dexteritytextindexer.searchable('function')
    function = schema.TextLine(
        title=_(u'label_function', default=u'Function'),
        missing_value=u"",
        default=u"",
        required=False)

    show_address = schema.Bool(
        title=_(u'label_show_address', default=u'Show address'),
        required=False)

    show_image = schema.Bool(
        title=_(u'label_show_image', default=u'Show image'),
        required=False)

    acquire_address = schema.Bool(
        title=_(u'label_acquire_address', default=u'Acquire address'),
        required=True)

    dexteritytextindexer.searchable('address')
    address = schema.Text(
        title=_(u'label_address', default=u'Address'),
        missing_value=u"",
        default=u"",
        required=False)

    dexteritytextindexer.searchable('postal_code')
    postal_code = schema.TextLine(
        title=_(u'label_postal_code', default=u'Postal code'),
        missing_value=u"",
        default=u"",
        required=False)

    dexteritytextindexer.searchable('city')
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        missing_value=u"",
        default=u"",
        required=False)

    dexteritytextindexer.searchable('email')
    email = RFC822MailAddress(
        title=_(u'label_email', default=u'E-Mail'),
        missing_value=u"",
        required=False)

    dexteritytextindexer.searchable('phone_office')
    phone_office = schema.TextLine(
        title=_(u'label_phone_office', default=u'Office phone number'),
        missing_value=u"",
        default=u"",
        required=False)

    dexteritytextindexer.searchable('phone_mobile')
    phone_mobile = schema.TextLine(
        title=_(u'label_phone_mobile', default=u'Mobile phone number'),
        missing_value=u"",
        default=u"",
        required=False)

    dexteritytextindexer.searchable('fax')
    fax = schema.TextLine(
        title=_(u'label_fax', default=u'Fax number'),
        missing_value=u"",
        default=u"",
        required=False)

    www = schema.URI(
        title=_(u'label_www', default=u'www'),
        missing_value=u"",
        required=False)

    model.fieldset(
        'contact',
        label=_(u'label_fieldset_contact', default=u"Contact"),
        fields=[
            'show_image',
            'acquire_address',
            'address',
            'postal_code',
            'city',
            'phone_office',
            'phone_mobile',
            'fax',
            'email',
            'www']
    )


class MemberBlock(Item):
    """A member
    """
    implements(IMemberBlock)

    def organization(self):
        return get_organization(
            self, ['OrgUnit', 'ftw.simplelayout.ContentPage'])
