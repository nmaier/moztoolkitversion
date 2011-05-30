try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import moztoolkitversion

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: GNU General Public License (GPL)",
               "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
               "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Software Development :: Libraries :: Python Modules",
               "Topic :: Software Development :: Testing"
               ]

docstrings = moztoolkitversion.__doc__.split("\n")

setup(name="mozilla-toolkitversion",
      version=moztoolkitversion.__version__,

      author="Nils Maier",
      author_email="maierman@web.de",
      license="MPL 1.1/GPL 2.0/LGPL 2.1",
      url="https://github.com/nmaier/moztoolkitversion",
      classifiers=classifiers,
      description=docstrings[0],
      long_description="\n".join(docstrings[1:]).strip(),

      platforms=["any"],
      packages=["moztoolkitversion"],
      package_data = {"tests": "*.py"},

      tests_require=["nose"],
      test_suite="nose.collector"
      )
