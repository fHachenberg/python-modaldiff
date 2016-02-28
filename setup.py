from setuptools import setup

import re

def cat_readme():
    with open('README.rst') as f:
        return f.read()

def grep_version():
    with open('modaldiff/modaldiff.py') as f:
        return re.search('^__version__\s*=\s*"(.*)"',
                         f.read(), re.M).group(1)

setup(name='python-modaldiff',
      version=grep_version(),
      description='Modal difference implemented in Python',
      long_description=cat_readme(),
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing',
      ],
      keywords='diff test',
      url='http://github.com/fHachenberg/python-modaldiff',
      author='Fabian Hachenberg',
      author_email='fabian.hachenberg@gmx.de',
      license='MIT',
      packages=['modaldiff'],
      entry_points = {
            "console_scripts": ['modaldiff = modaldiff.modaldiff:main']
                     },
      zip_safe=False,

      setup_requires=['pytest-runner'],
      tests_require=['pytest'],)
