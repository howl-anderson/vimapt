import enum


class ManageAction(enum.Enum):
    INSTALL = 'install'
    UNINSTALL = 'uninstall'
    UPDATE = 'update'