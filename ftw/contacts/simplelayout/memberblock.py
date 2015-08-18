from ftw.simplelayout.browser.blocks.base import BaseBlock
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.contacts.utils import get_contact_title
from ftw.contacts.browser.member import MemberView


class MemberBlockView(BaseBlock, MemberView):

    template = ViewPageTemplateFile('memberblock.pt')

    @property
    def image_caption(self):
        mtool = getToolByName(self, "portal_membership")

        if mtool.checkPermission('View', self.context.contact):
            return self.contact_title
        return ''

    @property
    def contact_title(self):
        return get_contact_title(
            self.context.contact.to_object, format='natural')
