from setuptools import setup

setup(
    name='hasty_python',
    version='1.0',
    description='this is a python package to interface with the hasty API',
    url='https://github.com/hasty-ai/hasty-python/',
    author='Kostya, Maxime Ellerbach',
    licence='MIT License',
    packages=['hasty'],
    install_requires=['requests >= 2.23.0']
)
