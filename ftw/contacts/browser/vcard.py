from Products.Five.browser import BrowserView
from ftw.contacts.interfaces import IContactsSettings
from ftw.contacts.utils import encode
from ftw.contacts.utils import generate_vcard
from plone import api


class DownloadVCardView(BrowserView):
    """Download vCard of contact
    """
    def __call__(self):

        try:
            encoding = api.portal.get_registry_record(
                name='vcard_encoding',
                interface=IContactsSettings,
                default=u'Windows-1252')
        except KeyError:
            encoding = u'Windows-1252'
        response = self.request.response
        response.setHeader("Content-type", "text/vcard")
        filename = encode('%s.vcf' % self.context.Title())
        response.setHeader("Content-Disposition",
                           'inline; filename="%s"' % filename)
        return generate_vcard(self.context, encoding=encoding).getvalue()
