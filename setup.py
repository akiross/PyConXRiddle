import sys
from setuptools import setup, find_packages
from pkg_resources import parse_requirements


with open("requirements.txt", 'r') as inst_reqs:
    install_requires = [req.split(';')[0] for req in inst_reqs.read().split('\n') if not req.startswith('-')]

with open("requirements-dev.txt", 'r') as test_reqs:
    tests_require = [req.split(';')[0] for req in test_reqs.read().split('\n')  if not req.startswith('-')]

packages = find_packages(include=['riddle', 'riddle.*'])

setup(
    name='riddle',
    version='0.2.0-dev-dev',
    url='https://github.com/akiross/PyConXRiddle',
    license='LICENSE',
    description='riddle framework',
    long_description=__doc__,
    packages=packages,
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
)