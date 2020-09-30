from ftw.upgrade import UpgradeStep
from Products.CMFPlone.utils import getFSVersionTuple

PLONE5 = getFSVersionTuple() >= (5, 0)


class RemoveObosleteBehaviourInPlone5(UpgradeStep):
    """Remove oboslete behaviour in Plone 5.
    """

    def __call__(self):
        if PLONE5:
            self.install_upgrade_profile()
