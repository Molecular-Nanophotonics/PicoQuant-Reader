import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pqreader",
    version="0.0.1",
    author="Martin",
    author_email="martin.fraenzl@physik.uni-leipzig.de",
    description="Package for reading files from PicoQuant TimeHarp 200",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/molecular-nanophotonics/pqreader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #python_requires='>=3.6',
)
