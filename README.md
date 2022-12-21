# Pytables-mapping

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Pytables-mapping - a simple mapping for pytables objects: tables, arrays, complex custom structures.

Inspired by Django ORM and [SimpleTable](https://www.pytables.org/cookbook/simple_table.html)


##Installation

Install and update using `pip`:

```
pip install git+https://github.com/antonkonovalov1976/pytables-mapping.git -U
```

##Requirements

* Python 3.6+
* A supported version of PyTables 3.7


##A simple example:
```python
import numpy as np
import pytables_mapping as mapping

class PythagoreanTriplesTable(mapping.Table):
    """Pythagorean triples table."""
    FULL_NODE_PATH = '/sequences'
    OBJECT_NAME = 'pythagorean_triples'
    DESCRIPTION = np.dtype([
        ('A', np.int64),
        ('B', np.int64),
        ('C', np.int64)])

class MainStore(mapping.HDF5Store):
    STORE_VERSION = 1
    semi_primes = PythagoreanTriplesTable()

if __name__ == '__main__':
    with MainStore('data.h5') as store:
        print(store.semi_primes.read())
```

##N.B.

To choose correct compression options see:
http://www.pytables.org/usersguide/libref/helper_classes.html#the-filters-class

and benchmarks:
http://alimanfoo.github.io/2016/09/21/genotype-compression-benchmark.html


##LINKS
* License: [MIT](https://github.com/antonkonovalov1976/pytables-mapping/blob/master/LICENSE)
* Code: https://github.com/antonkonovalov1976/pytables-mapping
* Issue tracker: https://github.com/antonkonovalov1976/pytables-mapping/issues
* Python: http://python.org/


