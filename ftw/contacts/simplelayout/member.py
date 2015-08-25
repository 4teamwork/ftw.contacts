from ftw.contacts.interfaces import IMemberAccessor
from ftw.contacts.utils import safe_html
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class MemberView(BrowserView):
    """View to display a member
    """
    def memberaccessor(self):
        return IMemberAccessor(self.context)

    @property
    def has_permission(self):
        mtool = getToolByName(self.context, "portal_membership")
        return bool(
            mtool.checkPermission("Modify portal content", self.context))

    @property
    def has_related_contact(self):
        return bool(self.context.contact.to_object)

    def safe_html(self, text):
        return safe_html(text)
