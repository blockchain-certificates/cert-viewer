import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='certificate-viewer',
    version='0.0.1',
    url='https://github.com/ml-learning/coins.media.mit.edu',
    license='MIT',
    author='MIT Media Labs certificates',
    author_email='coins@media.mit.edu',
    description='',
    packages=['certificate_viewer'],
    include_package_data=True,
    install_requires=[
        'docopt==0.4.0',
        'Flask==0.10.1',
        'Flask-PyMongo==0.4.1',
        'Flask-WTF==0.12',
        'itsdangerous==0.24',
        'Jinja2==2.7.3',
        'mandrill==1.0.57',
        'MarkupSafe==0.23',
        'pymongo>=3.0',
        'python-bitcoinlib==0.5.0',
        'requests==2.8.1',
        'Werkzeug==0.10.4',
        'WTForms==2.0.2',
        'mock==2.0.0',
        'mongomock==2.0.0',
        'tox==2.3.1'
    ], )