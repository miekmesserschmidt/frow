from setuptools import setup, find_packages, find_namespace_packages
import pathlib

import pkg_resources
import setuptools

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='frow',
    version='1.4.0',
    packages=find_packages(),    
    install_requires=install_requires,
    
    include_package_data = True,
    package_data={'frow': ['suite/*.pdf']},
)