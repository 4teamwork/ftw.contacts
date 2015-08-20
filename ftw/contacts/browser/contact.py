from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.utils import get_backreferences
from ftw.contacts.utils import safe_html
from plone import api
from Products.Five.browser import BrowserView


class ContactView(BrowserView):
    """Contact view
    """
    def get_memberships(self):
        return get_backreferences(self.context, IMemberBlock)

    def safe_html(self, text):
        return safe_html(text)


class ContactSummary(BrowserView):
    """Contactsummary view
    """
    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')

    def safe_html(self, text):
        return safe_html(text)
