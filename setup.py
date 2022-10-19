from setuptools import setup, find_packages
#~ import os, sys, glob, fnmatch

setup(name="OpenOPC",
  version=2.0,
  download_url='https://github.com/ingenuitas/OpenOPC/zipball/master',
  description="This is a clone of http://openopc.sourceforge.net modified to be used with distutils",
  keywords='python, opc, openopc, opc-da, opc classic',
  url='http://openopc.sourceforge.net',
  license='GPLv2',
  packages = find_packages(include=['openop120'],exclude=['ez_setup']),
  zip_safe = False,
  )
