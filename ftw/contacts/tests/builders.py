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


builder_registry.register('contact', ContactBuilder)
