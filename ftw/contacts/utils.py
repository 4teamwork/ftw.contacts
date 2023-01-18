from Acquisition import aq_inner
from Acquisition import aq_parent
from base64 import b64encode
from plone import api
from plone.memoize import instance
from plone.namedfile.utils import stream_data
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from StringIO import StringIO
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unicodedata


ALPHABET = map(chr, range(ord('A'), ord('Z') + 1))
LETTERS = ALPHABET + ['#']


def encode(text, encoding='UTF-8'):
    if not text:
        return ''
    if isinstance(text, unicode):
        return text.encode(encoding)
    return text.decode('utf-8').encode(encoding)


def get_organization(context, portal_types=[]):
    """Traverse up to search a parent-object matching a portal_type
    If it reaches a portal_type, it returns its title.
    If it reaches the plone siteroot it returns an empty string
    """
    context = aq_inner(context)
    parent = aq_parent(context)
    while parent.portal_type not in portal_types:
        if IPloneSiteRoot.providedBy(parent):
            return ''
        parent = parent.aq_parent
    return parent.Title()


def safe_html(text):
    if not text:
        return ''

    if isinstance(text, unicode):
        text = text.encode('utf-8')

    ttool = api.portal.get_tool('portal_transforms')
    text = ttool.convertTo('text/x-html-safe', text).getData()

    # we need html br
    text = text.replace('\r\n', '<br />').replace('\n', '<br />')

    # we dont want p tags
    text = text.replace('<p>', '').replace('</p>', '')

    return text


def get_backreferences(source_object, from_interface):
    """
    Return back references from source object on specified attribute_name
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    mtool = api.portal.get_tool('portal_membership')

    result = []

    for rel in catalog.findRelations({
            'to_id': intids.getId(aq_inner(source_object)),
            'from_interfaces_flattened': from_interface}):

        try:
            obj = intids.queryObject(rel.from_id)
        except KeyError:
            # Happends if a deleted content does not get garbage collected
            # Details see https://community.plone.org/t/image-scale-blobs-no-cleaned-by-zeopack-after-removing-scalesdict/12214
            continue

        if obj is not None and mtool.checkPermission('View', obj):
            result.append(obj)
    return result


def get_contact_title(contact, display=None):
    """This function returns the contacttitle.

    The contact title is generated from the firstname and lastname
    or from the organization name. Depends on what fields are filled.
    """

    if contact.firstname and contact.lastname:
        if display == 'natural':
            return '%s %s' % (contact.firstname, contact.lastname)
        return '%s %s' % (contact.lastname, contact.firstname)
    return contact.organization or u"..."


def normalized_first_letter(text):
    """Normalizes the first letter of the text
    """
    text = make_sortable(text)
    return text[0].upper()


def make_sortable(text):
    """Makes the text sortable
    """
    text = text.lower()
    text = text.decode('utf-8')
    normalized = unicodedata.normalize('NFKD', text)
    text = u''.join(
        [c for c in normalized if not unicodedata.combining(c)])
    text = text.encode('utf-8')
    return text


class AlphabeticLetters(object):
    """Provides a function to generate letters with different attributes
    """
    def letters(self, current_letter, brains):
        """Returns a dict with all available letters and
        aditional infos for each letter.

        The dict has:

        label: the letter name
        has_contents: css-class if there are objs with the letter
        current: css-class if the letter is the current letter
        """
        letters_with_content = self._letters_with_content(brains)

        for letter in LETTERS:
            has_contents = letter in letters_with_content and \
                "withContent" or ''
            current = letter == current_letter and 'active' or ''
            yield {'label': letter,
                   'has_contents': has_contents,
                   'current': current}

    @instance.memoize
    def _letters_with_content(self, brains):
        letters = set([])
        for contactname in [brain.Title for brain in brains]:
            first_letter = normalized_first_letter(contactname)
            if first_letter in ALPHABET:
                letters.add(first_letter)
            else:
                letters.add('#')

        return sorted(letters, key=LETTERS.index)


def generate_vcard(contact, encoding='UTF-8'):
    # TODO: Refactoring
    io = StringIO()
    charset = 'CHARSET=' + encoding

    gender_map = {
        'm': 'M',
        'f': 'F',
        '': 'U'
    }

    def encoder(text):
        return encode(text, encoding=encoding)

    def addProp(name, value):
        if not value:
            return
        io.write('{0}:{1}\n'.format(encoder(name),value))

    addProp('BEGIN', 'VCARD')
    addProp('VERSION', '2.1')
    addProp('N;' + charset, '{0};{1};;{2}'.format(encoder(contact.lastname),
                                                  encoder(contact.firstname),
                                                  encoder(contact.salutation)))
    addProp('FN;' + charset, encoder(contact.title))
    addProp('GENDER', gender_map.get(encoder(contact.gender), ''))
    addProp('ORG;' + charset, encoder(contact.organization))
    addProp('ADR;TYPE=WORK;' + charset, ';;{0};{1};;{2};{3}'.format(
        encoder(contact.address.replace('\n', '\\n').replace('\r', '')),
        encoder(contact.city),
        encoder(contact.postal_code),
        encoder(contact.country)))
    addProp('EMAIL', encoder(contact.email))
    addProp('TEL;TYPE=WORK', encoder(contact.phone_office))
    addProp('TEL;TYPE=WORK;TYPE=CELL', encoder(contact.phone_mobile))
    addProp('TEL;TYPE=WORK;TYPE=FAX', encoder(contact.fax))
    addProp('URL;' + charset, encoder(contact.www))
    addProp('ROLE;' + charset, encoder(contact.function))
    addProp('TEL;TYPE=HOME', encoder(contact.phone_private))
    addProp('ADR;TYPE=HOME', ';;{0};{1};;{2};'.format(
        encoder(contact.address_private.replace(
            '\r\n', '\\n').replace('\r', '')),
        encoder(contact.city_private),
        encoder(contact.postal_code_private)))

    if contact.image:
        imgdata = StringIO()
        imgdata.write(stream_data(contact.image))
        addProp('PHOTO;ENCODING=B', b64encode(imgdata.getvalue()))

    addProp('END', 'VCARD')
    io.seek(0)

    return io


def portrait_img_tag(contact):
    scaler = contact.restrictedTraverse('@@images')
    return scaler.scale('image', scale='portrait', direction='down').tag()
