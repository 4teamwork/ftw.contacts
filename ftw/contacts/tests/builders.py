from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder
from plone.namedfile import NamedImage


class ContactFolderBuilder(DexterityBuilder):
    portal_type = 'ftw.contacts.ContactFolder'

builder_registry.register('contact folder', ContactFolderBuilder)


class ContactBuilder(DexterityBuilder):
    portal_type = 'ftw.contacts.Contact'

    def with_image(self):
        self.arguments["image"] = NamedImage('GIF89a;', filename=u'image.gif')
        return self

    def with_minimal_info(self, firstname, lastname):
        """Contact with ontly the required fields filled
        """
        self.arguments.update(
            lastname=lastname,
            firstname=firstname
            )

        return self

    def with_maximal_info(self, firstname, lastname):
        """Contact with all possible information
        """
        self.arguments.update(
            organization=u'Fant\xe0storg',
            gender='f',
            lastname=lastname,
            firstname=firstname,
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

        self.with_image()

        return self

builder_registry.register('contact', ContactBuilder)
