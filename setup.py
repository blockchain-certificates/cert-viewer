import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-viewer',
    version='2.0',
    url='https://github.com/blockchain-certificates/cert-viewer',
    license='MIT',
    author='Blockcerts',
    author_email='info@blockcerts.org',
    description='A web app for viewing and validating blockchain certificates on the Bitcoin blockchain',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs
)
