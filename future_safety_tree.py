
class FutureSafetyTree():

    def __init__(self):
        
        self.root = {"id": [0], "data": {}, "children": []}

    def add_node(self, data, id):

        pass

    def find_parent(self, id, parent=None, iteration_counter=None, max_depth=20):

            if parent is None:
                parent = self.root
            if iteration_counter is None:
                iteration_counter = 0
        

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



