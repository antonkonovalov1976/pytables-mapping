from __future__ import annotations

import os
import typing as ty
import unittest

from numpy import dtype

import pytables_mapping as mapping
import pytables_mapping.consts as consts
from pytables_mapping.tests.consts import *


class CustomTestCase(unittest.TestCase):

    TEST_FILE_NAME: ty.Optional[str] = None

    def setUp(self) -> None:
        assert self.TEST_FILE_NAME

    def tearDown(self) -> None:
        assert self.TEST_FILE_NAME
        if os.path.isfile(self.TEST_FILE_NAME):
            os.remove(self.TEST_FILE_NAME)


ARRAYS_PATH = '/arrays'


class TestStore(mapping.HDF5Store):

    STORE_VERSION = TEST_STORE_VERSION

    table = mapping.Table(TEST_TABLE_OBJECT_NAME, TEST_TABLE_PATH,
                          description=dtype([('int', TEST_TABLE_DTYPE)]),
                          expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS)
    array = mapping.Array(TEST_ARRAY_OBJECT_NAME, ARRAYS_PATH,
                          atom=TEST_ANY_ARRAY_ATOM, shape=TEST_ANY_ARRAY_SHAPE)
    carray = mapping.CArray(TEST_CARRAY_OBJECT_NAME, ARRAYS_PATH,
                            atom=TEST_ANY_ARRAY_ATOM,
                            expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                            shape=TEST_ANY_ARRAY_SHAPE,
                            filters=consts.DEFAULT_DATA_FILTER)
    earray = mapping.EArray(TEST_EARRAY_OBJECT_NAME, ARRAYS_PATH,
                            atom=TEST_ANY_ARRAY_ATOM,
                            expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                            shape=(0,),
                            filters=consts.DEFAULT_DATA_FILTER)
    vlarray = mapping.VLArray(TEST_VLARRAY_OBJECT_NAME, ARRAYS_PATH,
                              atom=TEST_ANY_ARRAY_ATOM,
                              expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                              filters=consts.DEFAULT_DATA_FILTER)


class HDF5StoreTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_FILE_NAME

    def test_store(self) -> None:
        with TestStore(TEST_FILE_NAME, mode='w') as store:
            stored_objects = [obj.name for obj in store.get_all_mappings()]
            self.assertEqual(set(stored_objects), set(TEST_OBJECTS))
            self.assertTrue(store.is_writable)
            self.assertEqual(store.filename, TEST_FILE_NAME)

        with TestStore(TEST_FILE_NAME) as store:
            stored_objects = [obj.name for obj in store.get_all_mappings()]
            self.assertEqual(set(stored_objects), set(TEST_OBJECTS))
            self.assertFalse(store.is_writable)
            self.assertEqual(store.attrs.STORE_VERSION, TEST_STORE_VERSION)

            with self.assertRaises(IOError):
                store.remove()
                TestStore(TEST_FILE_NAME)


if __name__ == '__main__':
    unittest.main()
