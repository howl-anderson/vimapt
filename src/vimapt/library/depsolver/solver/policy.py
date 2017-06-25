import collections

import six

from ..compat \
    import \
        OrderedDict
from ..errors \
    import \
        DepSolverError
from ..requirement \
    import \
        Requirement
from ..version \
    import \
        MaxVersion

R = Requirement.from_string

class DefaultPolicy(object):
    """A Policy class that implements 'reasonable' defaults.

    Its behavior is:

        1. when multiple candidates are available, pick up the highest version first
        2. if a package is provided directly, it takes precedence over
        providers (overruling 1.)
        3. if a package is already installed, it takes precendence over higher
        version (over-ruling 1.)
    """
    def _compute_prefered_packages_installed_first(self, pool, installed_map, package_ids):
        """Returns a package name -> package queue mapping, with each queue
        being priority-sorted.

        It puts packages already installed first

        Arguments
        ---------
        pool: Pool
            Pool instance used to resolve packages, provides, etc...

        Returns
        -------
        package_queue: dict
            package name -> sorted queue of package ids. 
        """
        package_name_to_package_ids = OrderedDict()
        for package_id in package_ids:
            package = pool.package_by_id(package_id)

            if not package.name in package_name_to_package_ids:
                package_name_to_package_ids[package.name] = collections.deque()

            if package_id in installed_map:
                package_name_to_package_ids[package.name].appendleft(package_id)
            else:
                package_name_to_package_ids[package.name].append(package_id)

        return package_name_to_package_ids

    def _print_package_queues(self):
        if package_queues:
            print("package queues:")
        else:
            print("empty package queues")
        for name in package_queues:
            print("\t%s: %s" % (name, package_queues[name]))

    def select_preferred_packages(self, pool, installed_map, decision_queue):
        """Return a list of preferred package ids to install for the given
        package ids list, sorted by priority (from highest to lowest)."""
        package_queues = \
            self._compute_prefered_packages_installed_first(pool, installed_map,
                decision_queue)

        def package_id_to_version(package_id):
            if package_id in installed_map:
                return MaxVersion()
            else:
                package = pool.package_by_id(package_id)
                return package.version

        for package_name, package_queue in package_queues.items():
            sorted_package_queue = sorted(package_queue, key=package_id_to_version)[::-1]
            package_queues[package_name] = sorted_package_queue

        for package_name, package_queue in package_queues.items():
            package_queues[package_name] = prune_to_best_version(pool, package_queue)

        candidates = []
        for queue in six.itervalues(package_queues):
            candidates.extend(list(queue))

        return candidates

    def find_updated_packages(self, pool, installed_map, package):
        packages = []

        for candidate in pool.what_provides(R(package.name)):
            if candidate != package:
                packages.append(candidate)

        return packages

    def cmp_by_priority_prefer_installed(self, pool, installed_map, a, b,
            required_package=None, ignore_replace=False):
        """
        Comparison function that gives priority to installed packages first, and
        then across repository priorities.
        """
        if id(a.repository) == id(b.repository):
            if not ignore_replace:
                if self._replaces(a, b):
                    return 1
                if self._replaces(b, a):
                    return -1

            if required_package is not None:
                raise NotImplementedError("required_package handling not implemented yet")

            if a.id > b.id:
                return 1
            elif a.id < b.id:
                return -1
            else:
                return 0
        else:
            if a.id in installed_map:
                return -1
            if b.id in installed_map:
                return 1

            if self._priority(pool, a) > self._priority(pool, b):
                return -1
            else:
                return 1

    def _priority(self, pool, package):
        return pool.repository_priority(package.repository)

    def _replaces(self, source, target):
        for replace in source.replaces:
            if replace.name == target.name:
                return True
        return False

def prune_to_best_version(pool, package_ids):
    # Assume package_ids is already sorted (from max to min)
    if len(package_ids) < 1:
        return []
    else:
        best_package = pool.package_by_id(package_ids[0])
        best_version_only = [package_ids[0]]
        for package_id in package_ids[1:]:
            package = pool.package_by_id(package_id)
            if package.version < best_package.version:
                break
            else:
                best_version_only.append(package_id)

        return best_version_only
