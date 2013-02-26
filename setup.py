
from setuptools import setup, find_packages

setup(
		name = "canape.sdb",
		version="0.1.0",
		namespace_packages=['canape.sdb'],
		packages = find_packages('.'),
		package_dir = {'':'.'},
		zip_safe = False,
		
		entry_points = {'console_scripts': ['canape.sdb = canape.sdb.serve:main' ] },
		
		description = "canape sdb",
		author = "gclover",
		author_email = "clover.gch@gmail.com",
		
		license = "",
		keywords = (),
		platforms = "Independant",
		url = "",
	)

