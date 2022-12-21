"""Base classes for mapping stored objects in HDF-tree."""
from __future__ import annotations

import typing as ty

import numpy as np
import tables as tb


__all__ = [
    'BaseStoredObjectMapper',
    'Table',
    'Array',
    'CArray',
    'EArray',
    'VLArray'
]


NumPyKey = ty.Union[
    int, slice,
    ty.Tuple[ty.Union[int, slice], ...],
    np.ndarray
]

NumPyValue = ty.Union[int, float, bool, np.ndarray,
                      ty.Tuple[ty.Union[int, float, bool], ...]]


class BaseStoredObjectMapper:
    """Base class for all objects in the HDF storage tree."""

    # There are common params for create pytable datasets
    BYTEORDER: ty.Optional[str] = None
    FULL_NODE_PATH: ty.Optional[str] = None
    OBJ: ty.Optional[ty.Any] = None
    OBJECT_NAME: ty.Optional[str] = None
    TITLE: str = ''
    TRACK_TIMES: bool = True

    def __init__(self,
                 object_name: ty.Optional[str] = None,
                 full_node_path: ty.Optional[str] = None,
                 overwrite: bool = False,
                 **create_params: ty.Any) -> None:
        """Initialize the stored node object.

        :param object_name: The name of the node
        :type object_name: str or None
        :param full_node_path: path to node, e.g. '/folder/,my_table_91', etc,
        :type full_node_path: str or None
        :param overwrite: if True - the stored node will be removed when the
                            main instance is created
        :param create_params: specific params for Table, Array, CArray, etc,
        :type create_params: dict

        """
        self._object_name = object_name or self.OBJECT_NAME or ''
        self._full_node_path = full_node_path or self.FULL_NODE_PATH
        self._overwrite = overwrite
        self._obj = create_params.get('obj', self.OBJ)
        self._title = create_params.get('title', self.TITLE)
        self._byteorder = create_params.get('byteorder', self.BYTEORDER)
        self._track_times = create_params.get('track_times', self.TRACK_TIMES)
        (self._parent_node_path, self._node_name) = tb.path.split_path(
            self._full_node_path
        )
        self._node = None
        self._store = None
        self._create_params = create_params

    def reset_store(self, new_store: 'tb.file.File') -> None:
        """Reassign store of main mapper instance.

        :param new_store: PyTables file object
        """
        self._store = new_store
        self._node = None

    def __setitem__(self, key: NumPyKey, value: NumPyValue) -> None:
        """Set a row, a range of rows or a slice in the array."""
        if self._node is None:
            self.create()
        self._node.__setitem__(key, value)

    def __getitem__(self, key: NumPyKey) -> ty.Iterable[ty.Any]:
        """Get a row, a range of rows or a slice from the array."""
        return self._node.__getitem__(key)

    @property
    def create_params(self) -> ty.Dict[str, ty.Any]:
        """Return create params dictionary of stored object."""
        return self._create_params

    @property
    def name(self) -> str:
        """Return stored object name."""
        return self._object_name

    @property
    def node(self) -> ty.Optional[ty.Type['tb.Array']]:
        """Return table node object of current representation."""
        if self._store is None:
            return None
        if self._node is None:
            self._node = self._store.get_node(
                tb.path.join_path(self._full_node_path, self._object_name)
            )

        return self._node

    @property
    def parent_node(self) -> 'tb.group.RootGroup':
        """Return parent node object."""
        return self._store.get_node(self._parent_node_path)

    def create(self) -> None:
        """Set up mapping variables here with self.create_params."""
        assert self._store
        self._node = None

        if self._overwrite and self._full_node_path in self._store:
            self._store.remove_node(
                self._parent_node_path, self._node_name, recursive=True
            )

    def remove(self) -> None:
        """Remove current node with the same object in store object."""
        assert self._store
        self._node = None
        self._store.remove_node(self._full_node_path, self._object_name)

    @property
    def nrows(self) -> int:
        """Return count of rows in node object."""
        if self.node is not None:
            return self.node.nrows
        else:
            return 0


class Table(BaseStoredObjectMapper):
    """Mapping class for a numpy tables container."""

    CHUNKSHAPE: ty.Optional[int | ty.Tuple[int, ...]] = None
    EXPECTEDROWS: ty.Optional[int] = 10000
    FILTERS: ty.Optional['tb.Filters'] = None
    DESCRIPTION: ty.Optional[np.dtype] = None

    def append(self, sequence: np.ndarray) -> None:
        """Add a sequence of data to the end of the dataset."""
        if self._node is None:
            self.create()
        self._node.append(sequence)
        self._node.flush()

    def create(self) -> None:
        """Create the Table object in a store."""
        super().create()
        params = self.create_params
        self._node = self._store.create_table(
            self._full_node_path,
            self._object_name,
            description=params.get('description', self.DESCRIPTION),
            title=self._title,
            filters=params.get('filters', self.FILTERS),
            expectedrows=params.get('expectedrows', self.EXPECTEDROWS),
            chunkshape=params.get('chunkshape', self.CHUNKSHAPE),
            byteorder=self._byteorder,
            createparents=True,
            obj=self._obj,
            track_times=self._track_times
        )

    def read(self,
             start: ty.Optional[int] = None,
             stop: ty.Optional[int] = None,
             step: ty.Optional[int] = None,
             field: ty.Optional[str] = None,
             out: ty.Optional[np.ndarray] = None,
             default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Get data in the table as a (record) array.

        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int or None
        :param field: column name
        :type field: str or None
        :param out: an array to receive the output data
        :type out: numpy.ndarray
        :param default: default value that return if object node is not exists
        :type default: any type
        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read(start, stop, step, field, out)
        else:
            return default

    def read_where(self,
                   condition: str,
                   condvars: ty.Optional[ty.Dict] = None,
                   field: ty.Optional[str] = None,
                   start: ty.Optional[int] = None,
                   stop: ty.Optional[int] = None,
                   step: int = 1,
                   default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Read table data fulfilling the given *condition*.

        :param condition: string with condition expression, e.g. "
            (A > 0) & (A <= 20)'
        :type condition: str
        :param condvars: condvars should consist of identifier-like strings
        pointing to Column instances
        :type condvars: dict
        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int or None
        :param field: column name
        :type field: str or None
        :param default: default value that return if object node is not exists
        :type default: any type

        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read_where(condition, condvars, field, start,
                                         stop, step)
        else:
            return default


class Array(BaseStoredObjectMapper):
    """Mapping class for a pytables Array container."""

    ATOM: ty.Optional[ty.Type['tb.Atom']] = None
    SHAPE: ty.Optional[ty.Tuple[int, ...]] = None

    def create(self) -> None:
        """Create the Array object in a store."""
        super().create()
        params = self.create_params
        self._node = self._store.create_array(
            self._full_node_path,
            self._object_name,
            obj=self._obj,
            title=self._title,
            byteorder=self._byteorder,
            createparents=True,
            atom=params.get('atom', self.ATOM),
            shape=params.get('shape', self.SHAPE),
            track_times=self._track_times
        )

    def read(self,
             start: ty.Optional[int] = None,
             stop: ty.Optional[int] = None,
             step: ty.Optional[int] = None,
             out: ty.Optional[np.ndarray] = None,
             default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Get data in the Array as an object of the current flavor.

        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int or None
        :param out: an array to receive the output data
        :type out: numpy.ndarray
        :param default: default value that return if object node is not exists
        :type default: any type.
        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read(start, stop, step, out)
        else:
            return default


class CArray(BaseStoredObjectMapper):
    """Mapping class for a pytables CArray container."""

    ATOM: ty.Optional['tb.Atom'] = None
    CHUNKSHAPE: ty.Optional[int | ty.Tuple[int, ...]] = None
    SHAPE: ty.Optional[ty.Tuple[int]] = None
    FILTERS: ty.Optional['tb.Filters'] = None

    def create(self) -> None:
        """Create the CArray object in a store."""
        super().create()
        params = self.create_params
        self._node = self._store.create_carray(
            self._full_node_path,
            self._object_name,
            atom=params.get('atom', self.ATOM),
            shape=params.get('shape', self.SHAPE),
            title=self._title,
            filters=params.get('filters', self.FILTERS),
            chunkshape=params.get('chunkshape', self.CHUNKSHAPE),
            byteorder=self._byteorder,
            createparents=True,
            obj=self._obj,
            track_times=self._track_times
        )

    def read(self,
             start: ty.Optional[int] = None,
             stop: ty.Optional[int] = None,
             step: ty.Optional[int] = None,
             out: ty.Optional[np.ndarray] = None,
             default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Get data in the CArray as an object of the current flavor.

        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int or None
        :param out: an array to receive the output data
        :type out: numpy.ndarray
        :param default: default value that return if object node is not exists
        :type default: any type.
        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read(start, stop, step, out)
        else:
            return default


class EArray(BaseStoredObjectMapper):
    """Mapping class for a pytables EArray container."""

    ATOM: ty.Optional['tb.Atom'] = None
    CHUNKSHAPE: ty.Optional[int | ty.Tuple[int, ...]] = None
    SHAPE: ty.Optional[ty.Tuple[int]] = None
    EXPECTEDROWS: ty.Optional[int] = 1000
    FILTERS: ty.Optional['tb.Filters'] = None

    def append(self, sequence: np.ndarray) -> None:
        """Add a sequence of data to the end of the dataset."""
        if self._node is None:
            self.create()
        self._node.append(sequence)
        self._node.flush()

    def create(self) -> None:
        """Create the EArray object in a store."""
        super().create()
        params = self.create_params
        self._node = self._store.create_earray(
            self._full_node_path,
            self._object_name,
            atom=params.get('atom', self.ATOM),
            shape=params.get('shape', self.SHAPE),
            title=self._title,
            filters=params.get('filters', self.FILTERS),
            expectedrows=params.get('expectedrows', self.EXPECTEDROWS),
            chunkshape=params.get('chunkshape', self.CHUNKSHAPE),
            byteorder=self._byteorder,
            createparents=True,
            obj=self._obj,
            track_times=self._track_times
        )

    def read(self,
             start: ty.Optional[int] = None,
             stop: ty.Optional[int] = None,
             step: ty.Optional[int] = 1,
             out: ty.Optional[np.ndarray] = None,
             default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Get data in the EArray as an object of the current flavor.

        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int or None
        :param out: an array to receive the output data
        :type out: numpy.ndarray
        :param default: default value that return if object node is not exists
        :type default: any type.
        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read(start, stop, step, out)
        else:
            return default


class VLArray(BaseStoredObjectMapper):
    """Mapping class for a pytables VArray container."""

    ATOM: ty.Optional['tb.Atom'] = None
    CHUNKSHAPE: ty.Optional[int | ty.Tuple[int, ...]] = None
    EXPECTEDROWS: ty.Optional[int] = None
    FILTERS: ty.Optional['tb.Filters'] = None

    def append(self, sequence: np.ndarray) -> None:
        """Add a sequence of data to the end of the dataset."""
        if self._node is None:
            self.create()
        self._node.append(sequence)
        self._node.flush()

    def create(self) -> None:
        """Create the VLArray object in a store."""
        super().create()
        params = self.create_params
        self._node = self._store.create_vlarray(
            self._full_node_path,
            self._object_name,
            atom=params.get('atom', self.ATOM),
            title=self._title,
            filters=params.get('filters', self.FILTERS),
            expectedrows=params.get('expectedrows', self.EXPECTEDROWS),
            chunkshape=params.get('chunkshape', self.CHUNKSHAPE),
            byteorder=self._byteorder,
            createparents=True,
            obj=self._obj,
            track_times=self._track_times
        )

    def read(self,
             start: ty.Optional[int] = None,
             stop: ty.Optional[int] = None,
             step: ty.Optional[int] = 1,
             default: ty.Optional[ty.Collection] = None) -> ty.Any:
        """Get data in the VLArray as a list of objects of the current flavor.

        :param start: start value of range
        :type start: int or None
        :param stop: stop value of range
        :type stop: int or None
        :param step: step value of range
        :type step: int
        :param default: default value that return if object node is not exists
        :type default: any type.
        :rtype numpy.ndarray:
        """
        if self._node:
            return self._node.read(start, stop, step)
        else:
            return default
