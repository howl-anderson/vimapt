import networkx as nx


class Dependency(object):
    def __init__(self, package_name):
        self.package_name = package_name

        self.dependency_graph = nx.DiGraph()
        self.dependency_graph.add_node(self.package_name)
        self.top_node_name = self.package_name

    def parse(self, dependency_specification):
        node_name = self.get_node_name(dependency_specification)
        dependency_specification_list = self.get_dependency_specification_list(dependency_specification)
        for child_dependency_specification in dependency_specification_list:
            child_node_name = self.get_node_name(child_dependency_specification)
            self.dependency_graph.add_node(child_node_name)
            self.dependency_graph.add_edge(node_name, child_node_name)
            self.parse(child_dependency_specification)

    def get_dependency_specification_list(self, dependency_specification):
        return []

    def get_node_name(self, dependency_specification):
        return []