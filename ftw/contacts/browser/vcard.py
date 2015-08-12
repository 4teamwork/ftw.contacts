from base64 import b64encode
from plone.namedfile.utils import stream_data
from Products.Five.browser import BrowserView
from StringIO import StringIO
from ftw.contacts.utils import encode


class DownloadVCardView(BrowserView):
    """Download vCard of contact
    """
    def __call__(self):
        response = self.request.response
        response.setHeader("Content-type", "text/vcard")
        filename = encode('%s.vcf' % self.context.Title())
        response.setHeader("Content-Disposition",
                           'inline; filename="%s"' % filename)
        return self.generate_vcard(self.context).getvalue()

    def generate_vcard(self, contact):
        # TODO: Refactoring
        io = StringIO()

        gender_map = {
            'm': 'M',
            'f': 'F',
            '': 'U'
        }

        def addProp(name, value):
            if value not in (None, '', u''):
                io.write('{0}:{1}\n'.format(encode(name), encode(value)))

        addProp('BEGIN', 'VCARD')
        addProp('VERSION', '3.0')
        addProp('N', '{0};{1};;{2}'.format(encode(contact.lastname),
                                           encode(contact.firstname),
                                           encode(contact.salutation)))
        addProp('FN', encode(contact.title))
        addProp('GENDER', gender_map.get(encode(contact.gender), ''))
        addProp('ORG', encode(contact.organization))
        addProp('ADR;TYPE=WORK', ';;{0};{1};;{2};{3}'.format(
            encode(contact.address.replace('\n', '\\n').replace('\r', '')),
            encode(contact.city),
            encode(contact.postal_code),
            encode(contact.country)))
        addProp('EMAIL', encode(contact.email))
        addProp('TEL;TYPE=WORK', encode(contact.phone_office))
        addProp('TEL;TYPE=WORK;TYPE=CELL', encode(contact.phone_mobile))
        addProp('TEL;TYPE=WORK;TYPE=FAX', encode(contact.fax))
        addProp('URL', encode(contact.www))
        addProp('ROLE', encode(contact.function))
        addProp('TEL;TYPE=HOME', encode(contact.phone_private))
        addProp('ADR;TYPE=HOME', ';;{0};{1};;{2};'.format(
            encode(contact.address_private.replace('\r\n', '\\n').replace('\r', '')),
            encode(contact.city_private),
            encode(contact.postal_code_private)))

        if contact.image:
            imgdata = StringIO()
            imgdata.write(stream_data(contact.image))
            addProp('PHOTO;ENCODING=B', b64encode(imgdata.getvalue()))

        addProp('END', 'VCARD')
        io.seek(0)

        return io
