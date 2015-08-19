from Acquisition import aq_inner
from ftw.contacts.member import IMember
from Products.Five.browser import BrowserView
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


class ContactView(BrowserView):
    """Contact view
    """
    def get_memberships(self, source_object=None, attribute_name=None):
        """
        Return back references from source object on specified attribute_name
        """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        for rel in catalog.findRelations({
                'to_id': intids.getId(aq_inner(self.context)),
                'from_interfaces_flattened': IMember}):

            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result


class ContactSummary(BrowserView):
    """Contact view
    """
