from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class ContactFolderBuilder(DexterityBuilder):
    portal_type = 'ftw.contacts.ContactFolder'

builder_registry.register('contact folder', ContactFolderBuilder)


class ContactBuilder(DexterityBuilder):
    portal_type = 'ftw.contacts.Contact'

builder_registry.register('contact', ContactBuilder)
