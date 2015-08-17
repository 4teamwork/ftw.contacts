from ftw.contacts.interfaces import IMemberAccessor
from plone.api import user
from Products.Five.browser import BrowserView


class MemberView(BrowserView):
    """View to display a member
    """
    def __call__(self):
        if self.context.contact.to_object:
            return super(MemberView, self).__call__(self)

        if user.has_permission('Modify portal content', self.context):
            return "The related contact of this member does no longer exists"

        return ''

    def memberaccessor(self):
        return IMemberAccessor(self.context)
