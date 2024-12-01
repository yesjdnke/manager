from setuptools import setup, find_packages

setup(
    name='my_service_manager',
    version='1.0.0',
    description='A library to manage hidden service files by downloading, verifying, and running them.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yesjdnke/manager',  # Update with your repo
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)