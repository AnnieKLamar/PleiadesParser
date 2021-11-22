from distutils.core import setup
setup(
  name = 'PleiadesParser',
  packages = ['PleiadesParser'],
  version = '1.0',
  license='MIT',
  description = 'Downloads most recent data from Pleiades and parses data in to Python objects.',
  author = 'Annie K. Lamar',
  author_email = 'kalamar@stanford.edu',
  url = 'https://github.com/AnnieKLamar/PleiadesParser',
  download_url = 'https://github.com/AnnieKLamar/PleiadesParser/archive/refs/tags/v1.0.tar.gz',
  keywords = ['Pleiades', 'JSON', 'Stoa'],
  install_requires=[ 
          'wget',
          'json',
          'gzip',
          'shutil',
          'os'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)