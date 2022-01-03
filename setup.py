from setuptools import setup, Extension

get_directory_size = Extension(
    'oecommon_getsize',
    define_macros=[('MAJOR_VERSION', '1'),
                   ('MINOR_VERSION', '0')],
    include_dirs=['/usr/local/include'],
    libraries=[],
    library_dirs=[],
    sources=['Modules/oecommon_getsizemodule.cpp'],
    extra_compile_args=['-std=c++17']
)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    licence = f.read()

setup(
    name='oe_common',
    version='1.0.4',
    author='Dmitry Yakovlev',
    author_email='info@overhosting.ru',
    description='OeCommon',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    packages=['oe_common'],
    licence='MIT',
    ext_modules=[get_directory_size],
)
