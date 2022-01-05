from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    licence = f.read()

setup(
    name='oe_common',
    version='1.2.4',
    author='Dmitry Yakovlev',
    author_email='info@overhosting.ru',
    description='OeCommon',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    packages=['oe_common'],
    licence='MIT',
    url='https://github.com/jok4r/oe_common',
)
