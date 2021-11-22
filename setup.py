from distutils.core import setup
setup(
  name = 'PleiadesParser',
  packages = ['PleiadesParser'],
  version = '1.0',
  license='MIT',
  description = 'Downloads most recent data from Pleiades and parses data in to Python objects.',
  author = 'Annie K. Lamar',
  author_email = 'kalamar@stanford.edu',
  url = 'https://github.com/AnnieKLamar/PleiadesParser',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AnnieKLamar/PleiadesParser/src/PleiadesParser/PleiadesParser.py',    # I explain this later on
  keywords = ['Pleiades', 'JSON', 'Stoa'],
  install_requires=[            # I get to this in a second
          'wget',
          'json',
          'gzip',
          'shutil',
          'os'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)