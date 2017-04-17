from vimapt.transporter.Dispatcher import Dispatcher as TransporterDispatcher


class VimAptInstaller(object):
    def __init__(self, dot_vim_dir):
        self.dot_vim_dir = dot_vim_dir

    def install(self, package_name):
        self.init_check(package_file)
        self.check_repeat_install()
        self.check_depend()

    def download_package(self, package_name):
        transporter_dispatcher = TransporterDispatcher(self.dot_vim_dir)
        package_path_in_pool = transporter_dispatcher.dispatch().get_package(package_name)
