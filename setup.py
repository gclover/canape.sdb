
from setuptools import setup, find_packages
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob
import os


def main():

	print 'deleting generated files ...'
	os.system('rm -rf build')
	os.system('rm -rf ext/ring.cpp')

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

		cmdclass = {'build_ext' : build_ext},
                ext_modules = [
                        Extension('ring_',
                                ['ext/ring.pyx'] + glob.glob('ext/*.cpp'),
                                language = 'c++',
                        )
                ]
	)

if __name__ == '__main__':
	main()

