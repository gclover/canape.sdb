
from canape.sdb import Sdb



if __name__ == '__main__':

	db = Sdb(('localhost', 6000))

	for i in range(10000):
		db.put('k2' + str(i), 'v2' + str(i))
		db.get('k2' + str(i))

	db.close()






