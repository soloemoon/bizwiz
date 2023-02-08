from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='bizwiz',
    version='1.0A',
    author='Solomon', 
    author_email='soloemoon@gmail.com',
    packages=find_packages(),
    long_description=open('README.md').read()
)