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
    setup_requires=[
        "numpy>=1.16",
    ],
    install_requires=["numpy>=1.16", 'requests >= 2.23.0'],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
