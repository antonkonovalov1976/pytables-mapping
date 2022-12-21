from setuptools import find_packages
from setuptools import setup

import pytables_mapping


setup(
    name='pytables-mapping',
    version='.'.join([str(x) for x in pytables_mapping.__version__]),
    license=pytables_mapping.__license__,
    description='simple mapping for pytables objects: tables, arrays, custom '
                'complex custom structures',
    long_description=open('README.md').read(),
    author=pytables_mapping.__author__,
    author_email='anton.konovalov1976@gmail.com',
    url='https://github.com/antonkonovalov1976/pytables-mapping',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'numpy',
        'tables'
    ],
    keywords=['pytables', 'mapping', 'h5', 'hdf5'],
    python_requires='>=3.6',
    zip_safe=False,
    platforms='any'
)
