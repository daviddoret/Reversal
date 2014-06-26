__author__ = 'dmd'

from setuptools import setup

setup(
    name='Reversal',
    version='0.1.0',
    author='David Doret',
    author_email='david.doret@me.com',
    packages=['Reversal'],
    scripts=['main.py','test.py'],
    url=None,
    license='LICENSE.txt',
    description='Test package',
    long_description=open('README.txt').read(),
    install_requires=[
        "bitstring >= 3.1.3"
    ],
)

