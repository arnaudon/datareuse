from setuptools import find_packages, setup
from pathlib import Path

test_require = [
    "pyyaml",
    "dictdiffer",
    "pytest",
    "pytest-cov",
    "pytest-html",
]

setup(
    name="datareuse",
    author="Alexis Arnaudon",
    author_email="alexis.arnaudon@epfl.ch",
    version="0.0.3",
    description="Reuse computed datasets",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas>=1.0.2",
    ],
    extras_require={
        "all": test_require,
        "test": test_require,
    },
    packages=find_packages(),
)
