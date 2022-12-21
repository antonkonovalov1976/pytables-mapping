"""There are common constants for package."""

import tables as tb


DEFAULT_CHUNKSHAPE = 100
DEFAULT_EXPECTEDROWS = 10000

# compress options for regular data
DEFAULT_DATA_COMPLIB = 'blosc:lz4hc'
DEFAULT_DATA_COMPLEVEL = 3

# compress options for indexes
DEFAULT_INDEX_COMPLIB = 'blosc:lz4'
DEFAULT_INDEX_COMPLEVEL = 3

DEFAULT_COLUMNS_CHUNKSHAPE = (1000, )

DEFAULT_DATA_FILTER = tb.Filters(
    complevel=DEFAULT_DATA_COMPLEVEL,
    complib=DEFAULT_DATA_COMPLIB
)

DEFAULT_INDEX_FILTER = tb.Filters(
    complevel=DEFAULT_INDEX_COMPLEVEL,
    complib=DEFAULT_INDEX_COMPLIB
)
