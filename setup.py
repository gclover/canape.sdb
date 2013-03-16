
from setuptools import setup, find_packages
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob
import os


def main():

	setup(
		name = "canape.sdb",
		version="0.1.0",
		namespace_packages=['canape.sdb'],
		packages = find_packages('.'),
		package_dir = {'':'.'},
		zip_safe = False,
		
		entry_points = {'console_scripts': ['canape.sdb = canape.sdb.serve:serve'] },
		
		description = "canape sdb",
		author = "gclover",
		author_email = "clover.gch@gmail.com",
		
		license = "",
		keywords = (),
		platforms = "Independant",
		url = "",

	)

if __name__ == '__main__':
	main()

