from distutils.core import setup
from distutils.extension import Extension

import Cython.Build
import Cython.Compiler.Options

Cython.Compiler.Options.annotate = True

ext_modules = [
    Extension('minimize_thomson.minimize_thomson_c',
              sources=['./minimize_thomson/minimize_thomson_c.pyx'],
              libraries=['m'],
              )
]

setup(
    name='computational physics',
    packages=['minimize_thomson'],
    ext_modules=Cython.Build.cythonize(ext_modules, language_level=3)
)
