import codecs
import re
from setuptools import setup

with codecs.open("hasty/__init__.py") as file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        file.read(),
        re.MULTILINE,
    ).group(1)

setup(
    name='hasty',
    version=version,
    description='Hasty API client library',
    url='https://github.com/hasty-ai/hasty-python/',
    author='Hasty GmbH',
    author_email="herbert@hasty.ai",
    licence='MIT License',
    long_description_content_type="text/markdown",
    packages=['hasty'],
    install_requires=['numpy', 'requests >= 2.23.0']
)
