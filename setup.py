from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Recon243",
    version="1.0.0",
    author="Liuas25",
    author_email="liu25@example.com",
    description="Automated Reconnaissance & Vulnerability Scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liu25/Recon243",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Security Professionals",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests>=2.28.0",
        "rich>=13.0.0",
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.11.0",
        "dns-python>=2.2.0",
        "shodan>=1.29.0",
        "python-nmap>=0.7.1",
        "tldextract>=3.4.0",
        "colorama>=0.4.6",
        "jinja2>=3.1.0",
        "tabulate>=0.9.0",
        "python-whois>=0.8.0",
    ],
    entry_points={
        "console_scripts": [
            "recon243=recon243.__main__:main",
        ],
    },
    include_package_data=True,
)
