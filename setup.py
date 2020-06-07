import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fill5320",
    version="0.0.1",
    author="PrairieSnpr",
    author_email="midnryanmiller@gmail.com",
    description="A tool to fill ATF form 5320.20",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prairiesnpr/5320_filler",
    packages=setuptools.find_packages(),
    install_requires=["pdfforms", "PyPDF2", "reportlab"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
