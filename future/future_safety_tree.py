
import copy

# Tree data structure used by FutureSafety to store and navigate
# possible future snake positions across simulated turns.
class FutureSafetyTree():

    def __init__(self):
        
        self.root = {"id": [0], "data": None, "children": []}

    # Adds a new child node to the tree under the given parent.
    # Returns the new node's id which is derived from the parent's id.
    def add_node(self, data, parent_id):

        REQUIRED_KEYS = ["head", "body", "neck", "my_length"]
        if any(key not in data for key in REQUIRED_KEYS):
            raise KeyError("head, body, neck or my_length missing in data")

        try:
            parent = self.find_parent(parent_id)
        except RuntimeError:
            raise RuntimeError("Parent node not found")

        parent_children = parent["children"]
        parent_id = parent["id"]

        # child id extends parent id with its position in the children list
        child_id = parent_id + [len(parent_children) + 1]

        node = {
            "id": child_id,
            "data": {
                "head":      data["head"],
                "body":      data["body"],
                "neck":      data["neck"],
                "my_length": data["my_length"],
            },
            "children": [],
        }
        parent_children.append(node)

        return child_id

    # Recursively searches the tree for a node matching the given id.
    # The id is a list of indices representing the path from root to node.
    # Raises RuntimeError if the node is not found or max depth is exceeded.
    def find_parent(self, id, parent=None, iteration_counter=None, max_depth=20):

        if parent is None:
            parent = self.root
        if iteration_counter is None:
            iteration_counter = 1

        # root node requested
        if len(id) == 1 and id[-1] == 0:
            return self.root

        for child in parent.get("children", []):
            if iteration_counter > max_depth:
                raise RuntimeError("Max depth exceeded")

            try:
                child_id = child["id"]
            except KeyError:
                raise RuntimeError("Child node has no id")

            try:
                if child_id[-1] == id[iteration_counter]:
                    iteration_counter += 1
                    if iteration_counter < len(id):
                        # continue searching deeper in the tree
                        return self.find_parent(id, child, iteration_counter)
                    else:
                        # node found
                        return child
            except IndexError:
                raise RuntimeError("Invalid node id structure")

        raise RuntimeError("Node not found")
    
    # Creates the root node with the given data, preserving any existing children.
    def create_root(self, data):
        children = copy.deepcopy(self.root["children"])
        self.root = {"id": [0], "data": data, "children": children}

    # Resets the tree to an empty root node before a new simulation is started.
    def reset_tree(self):
        self.root = {"id": [0], "data": None, "children": []}
