from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.utils import get_backreferences
from ftw.contacts.utils import safe_html
from plone import api
from Products.Five.browser import BrowserView

# Check for ftw.geo
try:
    from collective.geo.geographer.interfaces import IGeoreferenceable
except ImportError:
    HAS_GEO_EXTRA = False
else:
    HAS_GEO_EXTRA = True


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
        return HAS_GEO_EXTRA and IGeoreferenceable.providedBy(self.context)


class ContactSummary(BrowserView):
    """Contactsummary view
    """
    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')

    def safe_html(self, text):
        return safe_html(text)
