from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scrap_stackoverflow",
    version="0.0.1",
    description="A package to scrap Stackoverflow website",
    py_modules=["scrapso"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/komus/stackoverflow-classification/tree/pypi_scrapping",
    author="Oyindolapo Komolafe",
    author_email="oyindolapokomolafe@yahoo.com",

    install_requires = [
        "beautifulsoup4 ~= 4.9.3",
        "requests ~= 2.25.1",
        "pandas ~= 1.3.0",
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
        ],
    },
)