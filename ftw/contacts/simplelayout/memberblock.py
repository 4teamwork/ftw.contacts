from ftw.contacts.simplelayout.member import MemberView
from ftw.contacts.utils import get_contact_title
from ftw.simplelayout.browser.blocks.base import BaseBlock
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MemberBlockView(BaseBlock, MemberView):

    template = ViewPageTemplateFile('templates/memberblock.pt')

    @property
    def image_caption(self):
        mtool = getToolByName(self, "portal_membership")

        if mtool.checkPermission('View', self.context.contact.to_object):
            return self.contact_title
        return ''

    @property
    def contact_title(self):
        return get_contact_title(
            self.context.contact.to_object, display='natural')
