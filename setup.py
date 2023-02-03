#! /usr/bin/env python

from setuptools import setup, Extension
from distutils.command.build_ext import build_ext as build_ext_orig
import importlib
import os

class CTypesExtension(Extension):
    pass

class build_ext(build_ext_orig):
    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + ".so"
        return super().get_ext_filename(ext_name)

# copied from kymatio's setup.py: https://github.com/kymatio/kymatio/blob/master/setup.py
pyrtools_version_spec = importlib.util.spec_from_file_location('pyrtools_version',
                                                               'pyrtools/version.py')
pyrtools_version_module = importlib.util.module_from_spec(pyrtools_version_spec)
pyrtools_version_spec.loader.exec_module(pyrtools_version_module)
VERSION = pyrtools_version_module.version


setup(
    name='pyrtools',
    version=VERSION,
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    description='Python tools for multi-scale image processing, including Laplacian pyramids, Wavelets, and Steerable Pyramids',
    license='MIT',
    url='https://github.com/LabForComputationalVision/pyrtools',
    author='Eero Simoncelli',
    author_email='eero.simoncelli@nyu.edu',
    keywords='multi-scale image-processing',
    packages=['pyrtools', 'pyrtools.pyramids', 'pyrtools.tools', 'pyrtools.pyramids.c'],
    package_data={'': ['*.h', 'LICENSE']},
    install_requires=['numpy>=1.1',
                      'scipy>=0.18',
                      'matplotlib>=1.5',
                      'Pillow>=3.4',
                      'tqdm>=4.29',
                      'requests>=2.21'],
    ext_modules=[CTypesExtension('pyrtools.pyramids.c.wrapConv',
                           sources=['pyrtools/pyramids/c/convolve.c',
                                    'pyrtools/pyramids/c/edges.c',
                                    'pyrtools/pyramids/c/wrap.c',
                                    'pyrtools/pyramids/c/internal_pointOp.c'],
                           depends=['pyrtools/pyramids/c/convolve.h',
                                    'pyrtools/pyramids/c/internal_pointOp.h'],
                           extra_compile_args=['-fPIC', '-shared'])],
                cmdclass={"build_ext":build_ext},
    tests='TESTS',
    )
