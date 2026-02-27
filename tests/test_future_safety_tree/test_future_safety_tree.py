
import unittest
from unittest.mock import patch , MagicMock

from future_safety_tree import FutureSafetyTree

class TestFutureSafetyTree(unittest.TestCase):

    def setUp(self):
        
        self.future_safety_tree = FutureSafetyTree("...")

        self.patchers = []

        self.addCleanup(self.stop_patchers)
    
    def setup_patchers(self, root):

        self.patchers.append(self.create_patcher_root(root))

        self.start_patchers()
    
    def create_patcher_root(self, root):

        patcher = patch.object(self.future_safety_tree, "root", new=root)
        return patcher
    
    def start_patchers(self):

        self.mocks = {}
        
        for i , patcher in enumerate(self.patchers):

            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                self.mocks[i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    def check_calls_patchers(self):

        for name , mock in self.mocks.items():

            try:
                mock.assert_called_once()
            except Exception:
                pass

    
    def test_find_parent(self):
        
            test_root = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}, {"id": [0 , 2], "data": "...", "children": []}]}

            self.setup_patchers(test_root)

            id = [0 , 2]
            
            result = self.future_safety_tree.find_parent([0 , 2])
            expected = {"id": [0 , 2], "data": "...", "children": []}
            
            self.check_calls_patchers()
            self.assertEqual(result, expected)

    def test_find_parent_more_iterations_necessary(self):
        
            test_root = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": [{"id": [0 , 1 , 1], "data": "...", "children": []}, {"id": [0 , 1 , 2], "data": "...", "children": [{"id": [0 , 1 , 2 , 1], "data": "...", "children": []}]}]}, {"id": [0 , 2], "data": "...", "children": [{"id": [0 , 2 , 1], "data": "...", "children": []}]}]}

            self.setup_patchers(test_root)
            
            id = [0 , 1 , 2 , 1]
            
            result = self.future_safety_tree.find_parent(id)
            expected = {"id": [0 , 1 , 2 , 1], "data": "...", "children": []}
            
            self.check_calls_patchers()
            self.assertEqual(result , expected)
    
    def test_find_parent_root(self):

        test_root = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}]}

        self.setup_patchers(test_root)

        id = [0]

        result = self.future_safety_tree.find_parent(id)
        expected = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}]}

        self.check_calls_patchers()
        self.assertEqual(result , expected)
    
    def test_find_parent_too_many_iterations(self):

        test_root = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}]}

        self.setup_patchers(test_root)

        id = [0 , 1]

        with self.assertRaises(RuntimeError):

            result = self.future_safety_tree.find_parent(id, iteration_counter=21)

        self.check_calls_patchers()


    def test_find_parent_not_found(self):

        test_root = {"id": [0], "data": "...", "children": [{"id": [0 , 1], "data": "...", "children": []}]}

        self.setup_patchers(test_root)

        id = [0 , 1 , 1]

        with self.assertRaises(RuntimeError):

            result = self.future_safety_tree.find_parent(id)

        self.check_calls_patchers()

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