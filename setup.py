from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="my_main_manager",
    version="1.0.8",
    author="yesjdnke",
    author_email="goaway@gmail.com",
    description="A Python package for managing hidden services.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use 'text/x-rst' if your README is RST
    url="https://github.com/yesjdnke/manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
