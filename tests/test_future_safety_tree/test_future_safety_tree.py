
import unittest
from unittest.mock import patch

from future_safety_tree import FutureSafetyTree

class TestFutureSafetyTree(unittest.TestCase):

    def setUp(self):
        
        self.future_safety_tree = FutureSafetyTree("...")
    
    def test_find_parent(self):

        test_root = {"id": 0, "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}, {"id": [0 , 2], "data": "...", "children": []}]}
        with patch.object(self.future_safety_tree, "root", new=test_root):

            id = [0 , 2]
            
            result = self.future_safety_tree.find_parent([0 , 2])
            expected = {"id": [0 , 2], "data": "...", "children": []}
            self.assertEqual(result, expected)

    def test_find_parent_root(self):

        pass
    
    def test_find_parent_too_many_iterations(self):

        pass

    def test_find_parent_id_not_found(self):

        pass

    def test_find_parent_keyerror_child_id(self):

        pass

    def test_find_parent_too_short_id(self):

        pass
    
    def test_add_node(self):

        pass

    def test_add_node_wrong_keys(self):

        pass

    def test_add_node_wrong_parent_keys(self):

        pass

    def test_reset_tree(self):

        pass

if __name__ == "__main__":

    unittest.main()