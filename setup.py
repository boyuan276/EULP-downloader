"""
Build and install the project.
"""
from setuptools import setup, find_packages


NAME = "eulp_downloader"
FULLNAME = "eulp_downloader"
AUTHOR = "Bo Yuan"
AUTHOR_EMAIL = "by276@cornell.edu"
MAINTAINER = "Bo Yuan"
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "BSD License"
URL = "https://github.com/boyuan276/EULP-downloader.git"
DESCRIPTION = "Python script for downloading End Use Load Profiles for U.S. Building Stock."
KEYWORDS = "eulp, end use load profiles, building stock, resstock, comstock"

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "Programming Language :: Python :: 3 :: Only",
]
PLATFORMS = "Any"
PACKAGES = find_packages()
# PACKAGES = find_packages(exclude=["old", "log_and_err"])
SCRIPTS = []
PACKAGE_DATA = {}
INSTALL_REQUIRES = [
    "numpy",
    "pandas",
    "requests",
    "pyarrow"
]
PYTHON_REQUIRES = ">=3.7"

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        scripts=SCRIPTS,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        python_requires=PYTHON_REQUIRES,
    )
