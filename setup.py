from distutils.core import setup
setup(
  name = 'PleiadesParser',
  packages = ['PleiadesParser'],
  version = '1.4',
  license='MIT',
  description = 'Downloads most recent data from Pleiades and parses data in to Python objects.',
  author = 'Annie K. Lamar',
  author_email = 'kalamar@stanford.edu',
  url = 'https://github.com/AnnieKLamar/PleiadesParser',
  download_url = 'https://github.com/AnnieKLamar/PleiadesParser/archive/refs/tags/v1.4.tar.gz',
  keywords = ['Pleiades', 'JSON', 'Stoa'],
  install_requires=[ 
          'wget'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
