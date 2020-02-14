from Acquisition import aq_inner, aq_parent
from ftw.contacts import _
from ftw.contacts import IS_PLONE_5
from ftw.contacts.interfaces import IMemberBlock
from ftw.contacts.utils import get_backreferences
from ftw.contacts.utils import safe_html
from ftw.contacts.utils import portrait_img_tag
from plone import api
from Products.Five.browser import BrowserView
from z3c.form.interfaces import HIDDEN_MODE


if IS_PLONE_5:
    from plone.app.content.browser.actions import RenameForm as PloneRenameForm

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
        memberships = get_backreferences(self.context, IMemberBlock)
        # Sort the memberships alphabetically by the title of their container before returning.
        return sorted(memberships, key=lambda membership: aq_parent(aq_inner(membership)).Title().lower())

    def safe_html(self, text):
        return safe_html(text)

    def show_map(self):
        """
        """
        return HAS_GEO_EXTRA and IGeoreferenceable.providedBy(self.context) and not self.context.hide_map

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

    def get_membership_url(self, memberblock):
        """
        Called from the template to construct the membership links so that
        the link points to the container of the memberblock and not the
        memberblock (obj) itself.
        """
        memberblock_container = aq_parent(aq_inner(memberblock))
        return memberblock_container.absolute_url() + '#' + memberblock.getId()


class ContactSummary(BrowserView):
    """Contactsummary view
    """

    def __call__(self):
        # Partial views are encoded wrong when not called by ajax in plone 5.
        # In consequece in tests, encoding errors can appear if we do not
        # disable the diazo theme 'encoder'.
        # Also see: https://github.com/4teamwork/ftw.testbrowser/commit/8ea19ffbefd251cd6712775336d2a1e76beb79de
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        return super(ContactSummary, self).__call__()

    def get_review_state(self):
        return api.content.get_state(obj=self.context, default='')

    def safe_html(self, text):
        return safe_html(text)

    @property
    def img_tag(self):
        return portrait_img_tag(self.context)


if IS_PLONE_5:
    class RenameForm(PloneRenameForm):
        """ Plone's standard RenameForm will try to """

        description = _(
            u'description_rename_contact',
            default=u"Each item has a Short Name which you can change by " +
                    u"entering the new details below (Note that the 'Title' of " +
                    u"a Contact is generated from other fields, so it can't be " +
                    u"changed here)."
        )

        def updateWidgets(self):
            super(RenameForm, self).updateWidgets()
            self.widgets["new_title"].mode = HIDDEN_MODE
