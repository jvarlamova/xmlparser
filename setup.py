from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='xmlparser',
    version='1.0',

    description='Demo project with simple xml parser.',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    author='Julia Odruzova',
    author_email='varlamova.ju@yandex.ru',

    install_requires=['futures==2.2.0', 'lxml', 'six'],
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'xmlparser = xmlparser.cli:main',
        ]
    }
)
