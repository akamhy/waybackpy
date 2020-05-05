import os.path
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name = 'waybackpy',
    packages = ['waybackpy'],
    version = 'v1.2',
    description = 'A python wrapper for Internet Archives Wayback Machine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author = 'akamhy',
    author_email = 'akash3pro@gmail.com',
    url = 'https://github.com/akamhy/waybackpy',
    download_url = 'https://github.com/akamhy/waybackpy/archive/v1.2.tar.gz',
    keywords = ['wayback', 'archive', 'archive website', 'wayback machine', 'Internet Archive'],
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',  
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',      
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
)
