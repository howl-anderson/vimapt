import subprocess

from vimapt.exception import VimaptAbortOperationException


class BaseHook(object):
    def __init__(self, vim_dir, package_path, package_name):
        self.vim_dir = vim_dir
        self.package_path = package_path
        self.package_name = package_name

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

        if return_code != 0:
            msg = "Pip package {} install failed!".format(package_specification)
            raise VimaptAbortOperationException(msg)

    def uninstall_pip_package(self, package_specification):
        try:
            import pip
        except ImportError:
            msg = "It seems there are no pip installation. But this package need pip support."
            raise VimaptAbortOperationException(msg)

        return_code = pip.main(['uninstall', package_specification])

        if return_code != 0:
            msg = "Pip package {} uninstall failed!".format(package_specification)
            raise VimaptAbortOperationException(msg)

    def process_execute(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        while process.poll() is None:
            line = process.stdout.readline()  # This blocks until it receives a newline.
            print(line)
        # When the subprocess terminates there might be unconsumed output
        # that still needs to be processed.
        print(process.stdout.read())