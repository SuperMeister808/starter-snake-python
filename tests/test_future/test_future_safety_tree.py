
import unittest
from unittest.mock import patch , MagicMock

from future.future_safety_tree import FutureSafetyTree

# Tests that FutureSafetyTree correctly adds nodes and finds parents by id.
class TestFutureSafetyTree(unittest.TestCase):

    def setUp(self):
        self.future_safety_tree = FutureSafetyTree()
        self.addCleanup(patch.stopall)

    def _patch_root(self, root):
        # patches the root node with the given test tree structure
        patch.object(self.future_safety_tree, "root", new=root).start()

    def test_find_parent(self):
        # verifies that a direct child node is found correctly
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
            {"id": [0, 2], "data": "...", "children": []},
        ]})

        result = self.future_safety_tree.find_parent([0, 2])
        self.assertEqual(result, {"id": [0, 2], "data": "...", "children": []})

    def test_find_parent_more_iterations_necessary(self):
        # verifies that a deeply nested node is found correctly
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": [
                {"id": [0, 1, 1], "data": "...", "children": []},
                {"id": [0, 1, 2], "data": "...", "children": [
                    {"id": [0, 1, 2, 1], "data": "...", "children": []},
                ]},
            ]},
            {"id": [0, 2], "data": "...", "children": [
                {"id": [0, 2, 1], "data": "...", "children": []},
            ]},
        ]})

        result = self.future_safety_tree.find_parent([0, 1, 2, 1])
        self.assertEqual(result, {"id": [0, 1, 2, 1], "data": "...", "children": []})

    def test_find_parent_root(self):
        # verifies that the root node is returned when id is [0]
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        result = self.future_safety_tree.find_parent([0])
        self.assertEqual(result, {"id": [0], "data": "...", "children": [{"id": [0, 1], "data": "...", "children": []}]})

    def test_find_parent_too_many_iterations(self):
        # verifies that RuntimeError is raised when max depth is exceeded
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        with self.assertRaises(RuntimeError):
            self.future_safety_tree.find_parent([0, 1], iteration_counter=21)

    def test_find_parent_not_found(self):
        # verifies that RuntimeError is raised when the node does not exist
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        with self.assertRaises(RuntimeError):
            self.future_safety_tree.find_parent([0, 1, 1])

    def test_find_parent_invalid_child_id(self):
        # verifies that RuntimeError is raised when a child has an invalid id type
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": "[0, 1]", "data": "...", "children": []},
        ]})

        with self.assertRaises(RuntimeError):
            self.future_safety_tree.find_parent([0, 1])

    def test_find_parent_too_short_id(self):
        # verifies that RuntimeError is raised when iteration counter exceeds id length
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        with self.assertRaises(RuntimeError):
            self.future_safety_tree.find_parent([0, 1], iteration_counter=3)

    def test_add_node(self):
        # verifies that a new node is added correctly and its id is returned
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        data = {"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"}
        result = self.future_safety_tree.add_node(data, [0, 1])

        self.assertEqual(result, [0, 1, 1])
        self.assertEqual(self.future_safety_tree.root, {
            "id": [0], "data": "...", "children": [
                {"id": [0, 1], "data": "...", "children": [
                    {"id": [0, 1, 1], "data": {"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"}, "children": []},
                ]},
            ],
        })

    def test_add_node_wrong_keys(self):
        # verifies that KeyError is raised when data is missing required keys
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        data = {"wrong_head": "head", "wrong_body": "body", "wrong_neck": "neck"}
        with self.assertRaises(KeyError):
            self.future_safety_tree.add_node(data, [0, 1])

    def test_add_node_wrong_parent_keys(self):
        # verifies that KeyError is raised when the parent node has invalid keys
        self._patch_root({"id": [0], "data": "...", "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        with patch.object(self.future_safety_tree, "find_parent",
                          return_value={"wrong_id": [0, 1], "data": "...", "wrong_children": []}):
            data = {"head": "head", "body": "body", "neck": "neck"}
            with self.assertRaises(KeyError):
                self.future_safety_tree.add_node(data, [0, 1])

    def test_reset_tree(self):
        # verifies that reset_tree clears all children and resets data to None
        self._patch_root({"id": [0], "data": None, "children": [
            {"id": [0, 1], "data": "...", "children": []},
        ]})

        self.future_safety_tree.reset_tree()
        self.assertEqual(self.future_safety_tree.root, {"id": [0], "data": None, "children": []})

if __name__ == "__main__":

    unittest.main()