"""Some test constants."""

from numpy import array
from numpy import int32
from numpy import int64
import tables as tb


TEST_STORE_VERSION = 42
TEST_FILE_NAME = '_temporary_test.h5'
TEST_ARRAY_FILE_NAME = '_temporary_arrays_test.h5'
TEST_CARRAY_FILE_NAME = '_temporary_carrays_test.h5'
TEST_EARRAY_FILE_NAME = '_temporary_earrays_test.h5'
TEST_VLARRAY_FILE_NAME = '_temporary_vlarrays_test.h5'
TEST_TABLES_FILE_NAME = '_temporary_tables_test.h5'

TEST_DATA_PATH = '/data'

TEST_TABLE_OBJECT_NAME = 'table'
TEST_ARRAY_OBJECT_NAME = 'array'
TEST_CARRAY_OBJECT_NAME = 'carray'
TEST_EARRAY_OBJECT_NAME = 'earray'
TEST_VLARRAY_OBJECT_NAME = 'vlarray'


TEST_OBJECTS = (
    TEST_TABLE_OBJECT_NAME,
    TEST_ARRAY_OBJECT_NAME,
    TEST_CARRAY_OBJECT_NAME,
    TEST_EARRAY_OBJECT_NAME,
    TEST_VLARRAY_OBJECT_NAME
)

TEST_TABLE_PATH = '/test_table'
TEST_TABLE_DTYPE = int64
TEST_TABLE = array([
    (3, 4, 5), (5, 12, 13),
    (7, 24, 25), (8, 15, 17),
    (9, 40, 41), (11, 60, 61),
    (12, 35, 37), (13, 84, 85),
    (15, 112, 113), (16, 63, 65),
    (17, 144, 145), (19, 180, 181),
    (20, 21, 29), (20, 99, 101),
    (21, 220, 221), (23, 264, 265),
    (24, 143, 145), (25, 312, 313),
    (27, 364, 365), (28, 45, 53),
    (28, 195, 197), (29, 420, 421),
    (31, 480, 481), (32, 255, 257),
    (33, 56, 65), (33, 544, 545),
    (35, 612, 613), (36, 77, 85),
    (36, 323, 325), (37, 684, 685),
], dtype=TEST_TABLE_DTYPE)
TEST_TABLE_LENGTH = len(TEST_TABLE)
TEST_EMPTY_TABLE = [(None, None, None), ]

TEST_TABLE_ROW = (555, 666, 777)

TEST_ANY_ARRAY_ATOM = tb.Int32Atom()
TEST_ANY_ARRAY_DTYPE = int32
TEST_ANY_ARRAY_EXPECTED_ROWS = 100
TEST_ANY_ARRAY_SHAPE = (TEST_ANY_ARRAY_EXPECTED_ROWS, )
TEST_ANY_ARRAY = array([4, 6, 9, 10, 14, 15, 21, 22, 25], TEST_ANY_ARRAY_DTYPE)
TEST_ANY_ARRAY_AS_LIST = list(TEST_ANY_ARRAY)
TEST_ANY_ARRAY_LENGTH = len(TEST_ANY_ARRAY)
