from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cmr/__init__.py
from cmr import __version__ as version

setup(
	name="cmr",
	version=version,
	description="Client Meeting Report App",
	author="Frutter Software Labs Private Limited",
	author_email="hello@frutterlabs.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
