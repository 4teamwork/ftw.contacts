from ftw.builder import Builder
from ftw.builder import create
from ftw.contacts.browser.vcard import DownloadVCardView
from ftw.contacts.testing import FTW_CONTACTS_FUNCTIONAL_TESTING
from unittest2 import TestCase
import os


def asset(filename):
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'assets', filename)
    with open(path, 'r') as file_:
        return file_.read()


class TextVCardExport(TestCase):
    layer = FTW_CONTACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_detailed_contact_works(self):
        contact = create(Builder('contact').having(
            organization=u'Fant\xe0storg',
            gender='f',
            lastname=u'M\xe9ier',
            firstname=u'Fr\xedtz',
            address=u'Chrache zw\xf6i',
            postal_code='1337',
            city=u'G\xf4tham',
            country='Schweiz',
            email='fmeier@stirnimaa.ch',
            phone_office='+41 33 456 78 01',
            phone_mobile='+70 98 765 43 21',
            fax='+41 33 456 78 02',
            www='http://www.cheib.ch',
            academic_title='Master of the Universe',
            function=u'Imk\xe9r',
            department=u'Cust\xf5mer Services',
            salutation='Sir',
            text=u'He is \xb1 awesome!',
            phone_private='+41 70 123 32 12',
            address_private='Chriesleweg 5',
            postal_code_private='9999',
            city_private='Dubai')
            .with_image())

        vcard_view = DownloadVCardView(contact, self.request)

        self.assertMultiLineEqual(asset('fritz-meier.vcf'), vcard_view())

    def test_minimal_contact_works(self):
        contact = create(Builder('contact').having(
            lastname='Blau',
            firstname='Minho'))

        vcard_view = DownloadVCardView(contact, self.request)

        self.assertMultiLineEqual(asset('blau-minho.vcf'), vcard_view())
