from setuptools import setup


setup(
    name='notes',
    version='0.0.1',
    py_modules=['notes'],
    install_requires=['requests', 'flask', 'sqlalchemy'],
    tests_require=['pytest'],
)
