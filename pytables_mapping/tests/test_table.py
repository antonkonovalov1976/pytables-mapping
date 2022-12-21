from __future__ import annotations

import unittest

from numpy import dtype
from tables.exceptions import NoSuchNodeError

from pytables_mapping.tests.consts import *
from pytables_mapping.tests.test_store import CustomTestCase
import pytables_mapping as mapping


class PythagoreanTriplesTable(mapping.Table):
    """Pythagorean triples table."""

    FULL_NODE_PATH = TEST_TABLE_PATH
    OBJECT_NAME = 'pythagorean_triples'
    DESCRIPTION = dtype([
        ('A', TEST_TABLE_DTYPE),
        ('B', TEST_TABLE_DTYPE),
        ('C', TEST_TABLE_DTYPE)])


class TestTableStore(mapping.HDF5Store):
    """Simple store for pythagorean triples data."""

    semi_primes = PythagoreanTriplesTable()


class TableMappingTestCase(CustomTestCase):

    TEST_FILE_NAME = TEST_TABLES_FILE_NAME

    def test_table(self) -> None:
        with TestTableStore(self.TEST_FILE_NAME, mode='w') as store:
            self.assertIsInstance(store.semi_primes.node, tb.Table)
            self.assertIsInstance(
                store.semi_primes.parent_node,
                tb.group.RootGroup)
            self.assertEqual(store.semi_primes.nrows, 0)
            self.assertEqual(
                store.semi_primes.read(default=TEST_EMPTY_TABLE),
                TEST_EMPTY_TABLE)
            store.semi_primes.append(TEST_TABLE)
            self.assertEqual(store.semi_primes.nrows, TEST_TABLE_LENGTH)
            self.assertEqual(
                len(store.semi_primes.read(step=2)),
                len(TEST_TABLE[::2]))
            self.assertEqual(tuple(store.semi_primes[0]), tuple(TEST_TABLE[0]))

            store.semi_primes[5] = TEST_TABLE_ROW
            self.assertEqual(tuple(store.semi_primes[5]), TEST_TABLE_ROW)

            fake_filtered_data = list(store.semi_primes.read_where(
                condition='(A > 0) & (A <= 1000)'))
            self.assertEqual(
                tuple(fake_filtered_data[0]),
                tuple(TEST_TABLE[0]))

        with TestTableStore(self.TEST_FILE_NAME) as store:
            self.assertEqual(store.semi_primes.nrows, TEST_TABLE_LENGTH)
            self.assertEqual(tuple(store.semi_primes[5]), TEST_TABLE_ROW)
            self.assertEqual(tuple(store.semi_primes[0]), tuple(TEST_TABLE[0]))

        with TestTableStore(self.TEST_FILE_NAME, mode='w') as store:
            store.semi_primes.remove()
            with self.assertRaises(NoSuchNodeError):
                _ = store.semi_primes.node
            with self.assertRaises(NoSuchNodeError):
                _ = store.semi_primes.nrows
            store.semi_primes.append(TEST_TABLE)
            self.assertEqual(store.semi_primes.nrows, TEST_TABLE_LENGTH)


if __name__ == '__main__':
    unittest.main()
