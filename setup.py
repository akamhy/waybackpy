import os.path
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name = 'waybackpy',
    packages = ['waybackpy'],
    version = 'v1.4',
    description = "A python wrapper for Internet Archive's Wayback Machine API. Archive pages and retrieve archived pages easily.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author = 'akamhy',
    author_email = 'akash3pro@gmail.com',
    url = 'https://github.com/akamhy/waybackpy',
    download_url = 'https://github.com/akamhy/waybackpy/archive/v1.4.tar.gz',
    keywords = ['wayback', 'archive', 'archive website', 'wayback machine', 'Internet Archive'],
    install_requires=[],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',      
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
        ],
)
