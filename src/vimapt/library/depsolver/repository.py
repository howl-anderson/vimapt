import collections

from .bundled.traitlets \
    import \
        HasTraits, Instance, List, Unicode
from .package \
    import \
        PackageInfo
from .version \
    import \
        Version

class Repository(HasTraits):
    """A repository is a container of packages.

    Parameters
    ----------
    packages: seq
        A sequence of packages
    """
    packages = List(Instance(PackageInfo))

    name = Unicode()

    def __init__(self, packages=None, name="", **kw):
        super(Repository, self).__init__(name=name, **kw)
        for p in packages or []:
            self.add_package(p)

    def __len__(self):
        return len(self.packages)

    def iter_packages(self):
        """Return an iterator over every package contained in this repo."""
        return iter(self.packages)

    def list_packages(self):
        """Return the list of every package contained in this repo."""
        return self.packages

    def add_package(self, package):
        """Add the given package to the repo.

        Parameters
        ----------
        package: PackageInfo
            PackageInfo to add.
        """
        # FIXME: setting up repository to package info is ugly.
        package.repository = self
        self.packages.append(package)

    def has_package(self, package):
        """Returns True if the given package is present in the repo, False
        otherwise.
        
        Parameters
        ----------
        package: PackageInfo
            PackageInfo to look for.
        """
        return self.find_package(package.name, package.version) is not None

    def has_package_name(self, name):
        """Returns True if one package with the given package name is present in
        the repo, False otherwise.
        
        Parameters
        ----------
        name: str
            package name to look for.
        """
        return len(self.find_packages(name)) > 0

    def find_package(self, name, version):
        """Find the package with the given name and version (exact match).

        Parameters
        ----------
        name: str
            Name of the package(s) to look for
        version: Version
            Version to look for.

        Returns
        -------
        package: PackageInfo or None
            The package if found, None otherwise.
        """
        ref = PackageInfo(name=name, version=version)
        for p in self.packages:
            if p.unique_name == ref.unique_name:
                return p
        return None

    def find_packages(self, name):
        """Returns a list of packages with the given name.

        Parameters
        ----------
        name: str
            Name of the package(s) to look for

        Returns
        -------
        packages: seq
            List of packages found (may be empty if no package found with the
            requested name).

        Notes
        -----
        Does not consider provides, e.g. if package A provides package B,
        find_packages(b_name) will not include A
        """
        return [p for p in self.packages if p.name == name]
