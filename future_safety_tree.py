
class FutureSafetyTree():

    def __init__(self, data):
        
        self.root = {"id": [0], "data": data, "children": []}

    def add_node(self, data, id):

        try:
            head = data["head"]
            body = data["body"]
            neck = data["neck"]
        except KeyError:
            raise KeyError("head, body oder neck nicht in data vorhanden")
        
        parent = self.find_parent(id)
        try:
            parent_children = parent["children"]
            parent_id = parent["id"]
        except KeyError:
            raise KeyError("key children oder id nicht in parent vorhanden")
        child_id = parent_id + [len(parent_children) + 1] 
        
        node = {"id": child_id, "head": head, "body": body, "neck": neck, "children": []}
        parent_children.append(node)

        return child_id

    def find_parent(self, id, parent=None, iteration_counter=None, max_depth=20):

            if parent is None:
                parent = self.root
            if iteration_counter is None:
                iteration_counter = 0
        
            if len(id) == 1:
                if id[-1] == 0:
                    return self.root

            for child in parent.get("children", []):
                if iteration_counter > max_depth:
                    raise RuntimeError("max depth überschritten")
                try:
                    child_id = child["id"]
                    if child_id[-1] == id[iteration_counter]:
                        iteration_counter += 1
                        if iteration_counter < len(id):
                            return self.find_parent(id, child, iteration_counter)
                        else:
                            return child
                except (KeyError, IndexError):
                    raise RuntimeError("child_id ungültig oder nicht vorhanden!")
                
            raise RuntimeError("Kein Parent gefunden!")
    
    def reset_tree(self):

        self.root = {"id": [0], "data": {}, "children": []}




