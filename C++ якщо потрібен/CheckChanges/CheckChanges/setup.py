import pybind11
from setuptools import setup, Extension

ext_modules = [
    Extension(
        'Pybind11Module',
        sources=['main.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['/std:c++17'],  # Прапор для MSVC
    )
]

setup(
    name='Pybind11Module',
    version='1.0',
    author='author',
    description='A C++ extension for algorithms',
    ext_modules=ext_modules,
    requires=['pybind11'],
)
