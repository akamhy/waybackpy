import os.path
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

about = {}
with open(os.path.join(os.path.dirname(__file__), "waybackpy", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    packages=["waybackpy"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    download_url="https://github.com/akamhy/waybackpy/archive/3.0.0.tar.gz",
    keywords=[
        "Archive Website",
        "Wayback Machine",
        "Internet Archive",
    ],
    install_requires=["requests", "click"],
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["waybackpy = waybackpy.cli:main"]},
    project_urls={
        "Documentation": "https://github.com/akamhy/waybackpy/wiki",
        "Source": "https://github.com/akamhy/waybackpy",
        "Tracker": "https://github.com/akamhy/waybackpy/issues",
    },
)
