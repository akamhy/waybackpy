import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = 'waybackpy',
  packages = ['waybackpy'],
  version = 'v1.2',
  long_description_content_type='text/markdown',
  long_description=long_description,
  license='MIT',
  description = 'A python wrapper for Internet Archives Wayback Machine',
  author = 'akamhy',
  author_email = 'akash3pro@gmail.com',
  url = 'https://github.com/akamhy/waybackpy',
  download_url = 'https://github.com/akamhy/waybackpy/archive/v1.2.tar.gz',
  keywords = ['wayback', 'archive', 'archive website', 'wayback machine', 'Internet Archive'],
  install_requires=[],
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
