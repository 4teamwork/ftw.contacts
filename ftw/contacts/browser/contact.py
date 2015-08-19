from ftw.contacts.member import IMember
from ftw.contacts.utils import get_backreferences
from plone import api
from Products.Five.browser import BrowserView


class ContactView(BrowserView):
    """Contact view
    """
    def get_memberships(self):
        return get_backreferences(self.context, IMember)


class ContactSummary(BrowserView):
    """Contactsummary view
    """
    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')
