import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SRE",
    version="1.0.0",
    author="Alexander Katyshev",
    author_email="amkatyshev97@gmail.com",
    description="Semantic Relation Extractor from russian texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amkatyshev/sre",
    packages=setuptools.find_packages(),
    install_requires=[
        "gensim",
        "ufal.udpipe",
        "pymorphy2",
        "conllu"
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)

