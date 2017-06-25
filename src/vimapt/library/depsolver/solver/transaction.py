import copy

import six

from ..bundled.traitlets \
    import \
        HasTraits, Instance, List
from ..compat \
    import \
        OrderedDict
from ..pool \
    import \
        Pool
from .decisions \
    import \
        DecisionsSet
from .operations \
    import \
        Operation, Install, Uninstall, Update
from .policy \
    import \
        DefaultPolicy

class Transaction(HasTraits):
    policy = Instance(DefaultPolicy)
    pool = Instance(Pool)
    decisions = Instance(DecisionsSet)

    installed_map = Instance(OrderedDict)

    _transactions = List(Instance(Operation))

    def __init__(self, pool, policy, installed_map, decisions, **kw):
        super(Transaction, self).__init__(pool=pool, policy=policy,
                installed_map=installed_map, decisions=decisions,
                _transactions=[], **kw)

    def compute_operations(self):
        self._transactions[:] = []

        install_means_update_map = self._find_updates()
        update_map = OrderedDict()
        install_map = OrderedDict()
        uninstall_map = OrderedDict()
        ignore_remove = OrderedDict()

        for decision in self.decisions:
            literal = decision.literal
            reason = decision.reason

            package_id = abs(literal)
            package = self.pool.package_by_id(package_id)

            # wanted & installed || !wanted & !installed
            if (literal > 0 and package_id in self.installed_map) or \
                (literal <= 0 and not package_id in self.installed_map):
                continue

            if literal > 0:
                if package_id in install_means_update_map:
                    source = install_means_update_map[package_id]

                    update_map[package_id] = {"package": package, "source": source, "reason": reason}
                    install_means_update_map.pop(package_id)
                    ignore_remove[source.id] = True

                else:
                    install_map[package_id] = {"package": package, "reason": reason}

        for decision in self.decisions:
            literal = decision.literal

            package_id = abs(literal)
            package = self.pool.package_by_id(package_id)

            if literal <= 0 and package_id in self.installed_map and \
               not package_id in ignore_remove:
                uninstall_map[package_id] = {"package": package, "reason": reason}

        self._transaction_from_maps(install_map, update_map, uninstall_map)
        return self._transactions

    def _find_updates(self):
        install_means_update_map = OrderedDict()

        for decision in self.decisions:
            literal = decision.literal
            package_id = abs(literal)
            package = self.pool.package_by_id(package_id)

            # !wanted & installed
            if literal <= 0 and package_id in self.installed_map:
                updates = self.policy.find_updated_packages(self.pool, self.installed_map, package)
                literals = [package_id]
                for update in updates:
                    literals.append(update.id)

                for update_literal in literals:
                    if update_literal != literal:
                        install_means_update_map[abs(update_literal)] = package

        return install_means_update_map

    def _find_root_packages(self, install_map, update_map):
        packages = copy.copy(install_map)
        packages.update(update_map)

        roots = packages

        for package_id, operation in six.iteritems(packages):
            package = operation["package"]

            if package_id in roots:
                for dependency in package.dependencies:
                    possible_requires = self.pool.what_provides(dependency)

                    for possible_require in possible_requires:
                        roots.pop(possible_require.id, None)

        return roots

    def _transaction_from_maps(self, install_map, update_map, uninstall_map):
        root_packages = six.itervalues(self._find_root_packages(install_map, update_map))
        queue = [operation["package"] for operation in root_packages]

        visited = set()

        while len(queue) > 0:
            package = queue.pop()
            package_id = package.id

            if not package_id in visited:
                queue.append(package)

                for dependency in package.dependencies:
                    possible_dependencies = self.pool.what_provides(dependency)

                    for possible_dependency in possible_dependencies:
                        queue.append(possible_dependency)

                visited.add(package_id)
            else:
                if package_id in install_map:
                    operation = install_map[package_id]
                    self._install(operation["package"], operation["reason"])
                    install_map.pop(package_id)

                if package_id in update_map:
                    operation = update_map[package_id]
                    self._update(operation["source"], operation["package"], operation["reason"])
                    update_map.pop(package_id)

        for operation in six.itervalues(uninstall_map):
            self._uninstall(operation["package"], operation["reason"])

    def _install(self, package, reason):
        self._transactions.append(Install(package, reason))

    def _update(self, source, package, reason):
        self._transactions.append(Update(source, package, reason))

    def _uninstall(self, package, reason):
        self._transactions.append(Uninstall(package, reason))
