import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dopyapi",
    version="0.0.1",
    author="Mouhsen Ibrahim",
    author_email="mouhsen.ibrahim@gmail.com",
    description="Python Library to access Digital Ocean API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohsenSy/dopyapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests',
        'requests-oauthlib'
    ]
    python_requires='>=3.6',
)
