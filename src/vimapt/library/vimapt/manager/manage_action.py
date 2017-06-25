import enum


class ManageAction(enum.Enum):
    INSTALL = 'install'
    UNINSTALL = 'uninstall'
    SOFT_UPDATE = 'soft_update'
    HARD_UPDATE = 'hard_update'
    UPDATE_ALL = 'update_all'
