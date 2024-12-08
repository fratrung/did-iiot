from setuptools import setup, find_packages
import did_iiot

setup(
    name="did_iiot",
    description="DID-IIoT is a Decentralized Identifier (DID) method specifically designed for Industrial Internet of Things (IIoT) environments",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Francesco Trungadi",
    author_email="francesco.trung@gmail.com",
    license="MIT",
    url="https://github.com/fratrung/did-iiot",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.5",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)