#!/usr/bin/env python3
"""Setup file for dell-printer-snmp module."""
from setuptools import setup

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", encoding="utf-8") as file:
    install_requires = list(val.strip() for val in file.readlines())

with open("requirements-test.txt", encoding="utf-8") as file:
    tests_require = list(val.strip() for val in file.readlines())

setup(
    name="dell_printer_snmp",
    version="1.0.0",
    author="Maciej Bieniek, kongo09",
    description="Python wrapper for getting data from Dell printers via SNMP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/kongo09/dell-printer-snmp",
    license="Apache-2.0 License",
    packages=["dell_printer_snmp"],
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
    setup_requires=("pytest-runner"),
    tests_require=tests_require,
)
