from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.utils import get_backreferences
from ftw.contacts.utils import safe_html
from plone import api
from Products.Five.browser import BrowserView

# Check for ftw.geo
try:
    from ftw.geo import interfaces
except ImportError:
    HAS_FTW_GEO = False
else:
    HAS_FTW_GEO = True


class ContactView(BrowserView):
    """Contact view
    """
    def get_memberships(self):
        return get_backreferences(self.context, IMemberBlock)

    def safe_html(self, text):
        return safe_html(text)

    def show_map(self):
        """
        """
        return HAS_FTW_GEO


class ContactSummary(BrowserView):
    """Contactsummary view
    """
    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')

    def safe_html(self, text):
        return safe_html(text)
