from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="my_service_manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for managing hidden services.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use 'text/x-rst' if your README is RST
    url="https://github.com/yourusername/my_service_manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
