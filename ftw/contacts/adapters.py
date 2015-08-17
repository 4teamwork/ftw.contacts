from Products.CMFPlone.utils import safe_unicode


class ContactLocationAdapter(object):
    """Adapter that is able to represent the location of Contact in
    a geocodable string form.
    """

    def __init__(self, context):
        self.context = context

    def getLocationString(self):
        """Build a geocodable location string from the Contact address
        related fields.
        """
        street = u' '.join(self.context.address.strip().split())
        # Remove Postfach from street, otherwise Google geocoder API will
        # return wrong results
        street = street.replace(u'Postfach', u'').replace(u'\r', u'').strip()
        zip_code = self.context.postal_code.strip()
        city = self.context.city.strip()
        country = self.context.country.strip()

        # We need at least something other than country to be defined,
        # otherwise we can't do a meaningful geocode lookup
        if not (street or zip_code or city):
            return None

        # Concatenate only the fields with a value into the location string
        location = country
        for field in [city, zip_code, street]:
            if not field:
                continue
            location = u"%s, %s" % (field, location)

        return location


class MemberAccessor(object):
    """Generic member accessor adapter implementation for Dexterity content
       objects.
    """
    def __init__(self, context):
        object.__setattr__(self, 'context', context)
        object.__setattr__(self, 'contact', context.contact.to_object)

    def __getattr__(self, name):
        if self.context.acquire_address and hasattr(self.contact, name):
            return getattr(self.contact, name, None)
        return getattr(self.context, name, None)

    def __setattr__(self, name, value):
        setattr(self.context, name, safe_unicode(value))
