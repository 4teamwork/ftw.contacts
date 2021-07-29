from ftw.upgrade import UpgradeStep


class AddVcardEncodingField(UpgradeStep):
    """Add vcard encoding field.
    """

    def __call__(self):
        self.install_upgrade_profile()
