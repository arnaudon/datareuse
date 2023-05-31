from setuptools import find_packages, setup

test_require = [
    "pyyaml",
    "dictdiffer",
    "pytest",
    "pytest-cov",
    "pytest-html",
]

setup(
    name="reuse",
    author="Alexis Arnaudon",
    author_email="alexis.arnaudon@epfl.ch",
    version="0.0.1",
    description="",
    install_requires=[
        "pandas>=1.0.2",
    ],
    extras_require={
        "all": test_require,
        "test": test_require,
    },
    packages=find_packages(),
)
