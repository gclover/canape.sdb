
from canape.sdb import Sdb
from canape.sdb import ClusterSdb


if __name__ == '__main__':

	sdb = Sdb(('localhost', 6000))

	for i in range(10000):
		sdb.put('k2' + str(i), 'v2' + str(i))
		sdb.get('k2' + str(i))

	sdb.close()


	nodes = [(), (), ()]
	sdb = ClusterSdb(nodes)
	
	for i in range(10000):
		sdb.put('', '')
	sdb.close()
	



