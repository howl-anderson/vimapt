from vimapt.exception import VimaptAbortOperationException


class BaseHook(object):
    def pre_install(self):
        return True

    def post_install(self):
        return True

    def pre_remove(self):
        return True

    def post_remove(self):
        return True

    def install_pip_package(self, package_specification):
        try:
            import pip
        except ImportError:
            msg = "It seems there are no pip installation. But this package need pip support."
            raise VimaptAbortOperationException(msg)

        return_code = pip.main(['install', package_specification])

        if return_code != 1:
            msg = "Pip package {} install failed!".format(package_specification)
            raise VimaptAbortOperationException(msg)

    def uninstall_pip_package(self, package_specification):
        try:
            import pip
        except ImportError:
            msg = "It seems there are no pip installation. But this package need pip support."
            raise VimaptAbortOperationException(msg)

        return_code = pip.main(['uninstall', package_specification])

        if return_code != 1:
            msg = "Pip package {} uninstall failed!".format(package_specification)
            raise VimaptAbortOperationException(msg)