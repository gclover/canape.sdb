
from canape.sdb import Sdb
from canape.sdb import ClusterSdb


def one():

	sdb = Sdb(('localhost', 6000))

	for i in range(100):
		sdb.put('k2' + str(i), 'v2' + str(i))
		sdb.get('k2' + str(i))

	sdb.close()


def multi():
	nodes = {'node1':('localhost', 6000)}
	sdb = ClusterSdb(nodes)
	
	for i in range(100):
		sdb.put('k2' + str(i), 'v2' + str(i))
		sdb.get('k2' + str(i))


	sdb.close()
	

if __name__ == '__main__':
	multi()
