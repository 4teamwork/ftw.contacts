from ftw.contacts.member import IMember
from ftw.contacts.utils import get_backreferences
from Products.Five.browser import BrowserView


class ContactView(BrowserView):
    """Contact view
    """
    def get_memberships(self):
        return get_backreferences(self.context, IMember)


class ContactSummary(BrowserView):
    """Contact view
    """
