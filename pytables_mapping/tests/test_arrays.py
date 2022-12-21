from __future__ import annotations

import unittest

from pytables_mapping.consts import DEFAULT_DATA_FILTER
from pytables_mapping.tests.consts import *
from pytables_mapping.tests.test_store import CustomTestCase
import pytables_mapping as mapping


class TestArrayStore(mapping.HDF5Store):

    ARRAY_PATH = '/arrays'
    array = mapping.Array(TEST_ARRAY_OBJECT_NAME, ARRAY_PATH,
                          atom=TEST_ANY_ARRAY_ATOM,
                          shape=TEST_ANY_ARRAY_SHAPE)


class TestCArrayStore(mapping.HDF5Store):

    ARRAY_PATH = '/arrays'
    carray = mapping.CArray(TEST_CARRAY_OBJECT_NAME, ARRAY_PATH,
                            atom=TEST_ANY_ARRAY_ATOM,
                            expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                            shape=TEST_ANY_ARRAY_SHAPE,
                            filters=DEFAULT_DATA_FILTER)


class TestEArrayStore(mapping.HDF5Store):

    ARRAY_PATH = '/arrays'
    earray = mapping.EArray(TEST_EARRAY_OBJECT_NAME, ARRAY_PATH,
                            atom=TEST_ANY_ARRAY_ATOM,
                            expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                            shape=(0,),
                            filters=DEFAULT_DATA_FILTER)


class TestVLArrayStore(mapping.HDF5Store):

    ARRAY_PATH = '/arrays'
    vlarray = mapping.VLArray(TEST_VLARRAY_OBJECT_NAME, ARRAY_PATH,
                              atom=TEST_ANY_ARRAY_ATOM,
                              expected_rows=TEST_ANY_ARRAY_EXPECTED_ROWS,
                              filters=DEFAULT_DATA_FILTER)


class ArraysMappingTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_ARRAY_FILE_NAME

    def test_array(self) -> None:
        with TestArrayStore(self.TEST_FILE_NAME, mode='w') as store:
            self.assertIsInstance(store.array.node, tb.Array)
            self.assertIsInstance(store.array.parent_node, tb.group.RootGroup)
            self.assertEqual(store.array.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)
            store.array[0:TEST_ANY_ARRAY_LENGTH] = TEST_ANY_ARRAY
            self.assertEqual(store.array.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)

        with TestArrayStore(self.TEST_FILE_NAME) as store:
            self.assertEqual(store.array.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)
            data1 = list(store.array[0:TEST_ANY_ARRAY_LENGTH])
            data2 = list(store.array.read(stop=TEST_ANY_ARRAY_LENGTH))
            self.assertEqual(data1, TEST_ANY_ARRAY_AS_LIST)
            self.assertEqual(data2, TEST_ANY_ARRAY_AS_LIST)


class CArraysMappingTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_CARRAY_FILE_NAME

    def test_array(self) -> None:
        with TestCArrayStore(self.TEST_FILE_NAME, mode='w') as store:
            self.assertIsInstance(store.carray.node, tb.CArray)
            self.assertIsInstance(store.carray.parent_node, tb.group.RootGroup)
            self.assertEqual(store.carray.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)
            store.carray[0:TEST_ANY_ARRAY_LENGTH] = TEST_ANY_ARRAY
            self.assertEqual(store.carray.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)

        with TestCArrayStore(self.TEST_FILE_NAME) as store:
            self.assertEqual(store.carray.nrows, TEST_ANY_ARRAY_EXPECTED_ROWS)
            data1 = list(store.carray[0:TEST_ANY_ARRAY_LENGTH])
            data2 = list(store.carray.read(stop=TEST_ANY_ARRAY_LENGTH))
            self.assertEqual(data1, TEST_ANY_ARRAY_AS_LIST)
            self.assertEqual(data2, TEST_ANY_ARRAY_AS_LIST)


class EArraysMappingTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_EARRAY_FILE_NAME

    def test_earray(self) -> None:
        with TestEArrayStore(self.TEST_FILE_NAME, mode='w') as store:
            self.assertIsInstance(store.earray.node, tb.EArray)
            self.assertIsInstance(store.earray.parent_node, tb.group.RootGroup)
            self.assertEqual(store.earray.nrows, 0)
            store.earray.append(TEST_ANY_ARRAY)
            self.assertEqual(store.earray.nrows, TEST_ANY_ARRAY_LENGTH)

        with TestEArrayStore(self.TEST_FILE_NAME) as store:
            self.assertEqual(store.earray.nrows, TEST_ANY_ARRAY_LENGTH)
            data1 = list(store.earray[0:TEST_ANY_ARRAY_LENGTH])
            data2 = list(store.earray.read(stop=TEST_ANY_ARRAY_LENGTH))
            self.assertEqual(data1, TEST_ANY_ARRAY_AS_LIST)
            self.assertEqual(data2, TEST_ANY_ARRAY_AS_LIST)


class VLArraysMappingTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_VLARRAY_FILE_NAME

    def test_array(self) -> None:
        with TestVLArrayStore(self.TEST_FILE_NAME, mode='w') as store:
            self.assertIsInstance(store.vlarray.node, tb.VLArray)
            self.assertIsInstance(
                store.vlarray.parent_node,
                tb.group.RootGroup)
            self.assertEqual(store.vlarray.nrows, 0)
            store.vlarray.append(TEST_ANY_ARRAY)
            self.assertEqual(store.vlarray.nrows, 1)

        with TestVLArrayStore(self.TEST_FILE_NAME) as store:
            self.assertEqual(store.vlarray.nrows, 1)
            data1 = list(store.vlarray[0])
            data2 = list(store.vlarray.read()[0])
            self.assertEqual(data1, TEST_ANY_ARRAY_AS_LIST)
            self.assertEqual(data2, TEST_ANY_ARRAY_AS_LIST)


if __name__ == '__main__':
    unittest.main()
