import sys
from setuptools import setup
from setuptools import find_packages
requirements = ['keyring','getpass']
setup(
      name='Submit',
      version='0.1.0',
      description='Submit spoj solution through terminal',
      keywords='spoj Submit terminal submit solution',
      url='https://github.com/yashpal1995',
      author='Yashpal',
      author_email='yashpal.c1995@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['Submit = Submit:main'],
      },
      zip_safe=False)
