from enum import Enum


class HookType(Enum):
    PRE_INSTALL = 1
    POST_INSTALL = 2

    PRE_REMOVE = 3
    POST_REMOVE = 4

HookTypeToMethodNameMapping = {
    HookType.PRE_INSTALL: 'pre_install',
    HookType.POST_INSTALL: 'post_install',

    HookType.PRE_REMOVE: 'pre_remove',
    HookType.POST_REMOVE: 'post_remove'
}