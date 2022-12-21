"""Base classes for data storage implementation."""
from __future__ import annotations

import os
import typing as ty

import tables as tb

from pytables_mapping.mapping import BaseStoredObjectMapper


T = ty.TypeVar('T', bound='HDF5Store')


class HDF5Store:
    """Base class for all hdf5-storages."""

    STORE_VERSION: ty.Optional[ty.Any] = None

    def __init__(self, filename: str, mode: str = 'r') -> None:
        """Initialize the store object.

        :param filename: The name of the file
        :param mode: The mode to open the file.
        """
        assert isinstance(filename, str), type(filename)
        self._hdf_store = tb.open_file(filename, mode=mode)
        self._reset()
        super().__init__()

    def _reset(self) -> None:
        for obj in self.get_all_mappings():
            obj.reset_store(self._hdf_store)
            if self.is_writable:
                obj.create()

    def reopen(self, filename: str, mode: str = 'r') -> None:
        """Reopen main storage with new path and/or mode.

        :param filename: The name of the file
        :param mode: The mode to open the file.
        """
        self._hdf_store = tb.open_file(filename, mode=mode)
        self._reset()

    @property
    def filename(self) -> str:
        """Return the name of the main storage file.

        :rtype str
        """
        return self._hdf_store.filename

    @property
    def is_writable(self) -> bool:
        """Run True if is the main storage file writable.

        :rtype bool
        """
        return self._hdf_store._iswritable()

    @property
    def attrs(self) -> 'tb.attributeset.AttributeSet':
        """Return hdf store root attributes object.

        It can be used for save something into H5-file
        """
        return self._hdf_store.root._v_attrs

    def get_all_mappings(self) -> ty.List[BaseStoredObjectMapper]:
        """Return all stored object as list.

        :rtype list
        """
        return [
            getattr(self, attr)
            for attr in dir(self)
            if isinstance(getattr(self, attr), BaseStoredObjectMapper)
        ]

    def __enter__(self: T) -> T:
        """Enter a context and return the same store object."""
        return self

    def __exit__(self, *exc_info: ty.Any) -> None:
        """Exit a context and close the main storage file."""
        self.close()

    def close(self) -> None:
        """Close the main storage file."""
        if self._hdf_store.isopen:
            if self._hdf_store._iswritable():
                self.attrs.STORE_VERSION = self.STORE_VERSION
                self._hdf_store.flush()
            self._hdf_store.close()

    def flush(self) -> None:
        """Flush all main store objects to disk."""
        self._hdf_store.flush()

    def remove(self) -> None:
        """Remove hdf5 store file if exists."""
        if os.path.isfile(self._hdf_store.filename):
            os.remove(self._hdf_store.filename)
