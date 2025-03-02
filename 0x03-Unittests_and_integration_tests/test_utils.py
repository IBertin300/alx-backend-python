#!/usr/bin/env python3
"""
Parameterize Unit testing
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """
    Test `access_nested_map` with various inputs.
    """
    @parameterized.expand([
        ({"a": 1}, ("a"), 1),
        ({"a": {"b": 2}}, ("a"), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nest, path, res):
        """
        Verify `access_nested_map` returns expected results.
        """
        self.assertEqual(access_nested_map(nest, path), res)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Verify `access_nested_map` raises `KeyError` for invalid paths.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    """
    Test `get_json` with various inputs.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Verify `get_json` makes GET requests and returns correct payload.
        """
        response = Mock()
        response.json.return_value = test_payload
        mock_get.return_value = response

        res = get_json(test_url)

        mock_get.assert_called_with(test_url)
        self.assertEqual(res, test_payload)

class TestMemoize(unittest.TestCase):
    """
    Test the `memoize` decorator.
    """
    def test_memoize(self):
        """
        Verify `memoize` caches the method result.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock_method:
            myobject = TestClass()

            myobject.a_property()
            myobject.a_property()

            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()
