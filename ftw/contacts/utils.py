def get_contact_title(contact, format=None):
    """This function returns the contacttitle.

    The contact title is generated from the firstname and lastname
    or from the organization name. Depends on what fields are filled.
    """
    if contact.firstname and contact.lastname:
        if format == 'natural':
            return '%s %s' % (contact.firstname, contact.lastname)
        return '%s %s' % (contact.lastname, contact.firstname)
    return contact.organization or u"..."
