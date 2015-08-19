from Acquisition import aq_inner
from plone.memoize import instance
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
import unicodedata


ALPHABET = map(chr, range(ord('A'), ord('Z') + 1))
LETTERS = ALPHABET + ['#']


def encode(text):
    if not text:
        return ''
    if isinstance(text, unicode):
        return text.encode('utf-8')
    return text


def get_backreferences(source_object, from_interface):
        """
        Return back references from source object on specified attribute_name
        """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        for rel in catalog.findRelations({
                'to_id': intids.getId(aq_inner(source_object)),
                'from_interfaces_flattened': from_interface}):

            obj = intids.queryObject(rel.from_id)

            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result


def get_contact_title(contact, format=None):
    """This function returns the contacttitle.

    The contact title is generated from the firstname and lastname
    or from the organization name. Depends on what fields are filled.
    """
    if contact.firstname and contact.lastname:
        if format == 'natural':
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
    """
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
            current = letter == current_letter and 'current' or ''
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
