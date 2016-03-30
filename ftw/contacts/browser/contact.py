from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.utils import get_backreferences
from ftw.contacts.utils import safe_html
from ftw.contacts.utils import portrait_img_tag
from plone import api
from Products.Five.browser import BrowserView

# Check for ftw.geo
try:
    from collective.geo.geographer.interfaces import IGeoreferenceable
    from collective.geo.mapwidget.browser.widget import MapWidget

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

    def get_address_map(self):
        address_map = MapWidget(self, self.request, self.context)
        address_map.mapid = "geo-%s" % self.context.getId()

        return address_map

    @property
    def portrait_css_class(self):
        css_class = 'contactPortrait {}'
        gender = self.context.gender
        gender_css_class = 'gender-{}'.format(gender)
        return css_class.format(gender_css_class)

    @property
    def img_tag(self):
        return portrait_img_tag(self.context)


class ContactSummary(BrowserView):
    """Contactsummary view
    """
    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')

    def safe_html(self, text):
        return safe_html(text)

    @property
    def img_tag(self):
        return portrait_img_tag(self.context)
