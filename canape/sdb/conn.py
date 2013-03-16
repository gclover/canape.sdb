
from gevent import socket
from canape.sdb import gutils
from canape.sdb.hashring import HashRing

class Sdb(object):

	def __init__(self, addr):
		self.sock = socket.socket()
		self.sock.connect(addr)

	def close(self):
		gutils.bye(self.sock)
		self.sock.close()

	def put(self, k, v):
		try:
			(ha, res) = gutils.sendrecv(self.sock, 'put', (k, v))
			if ha == 0:
				return res
		except Exception, e:
			print e	

	def get(self, k):
		try:
			(ha, res) = gutils.sendrecv(self.sock, 'get', k)
			if ha == 0:
				return res
		except Exception, e:
			print e
		
class ClusterSdb(object):
	
	def __init__(self, nodes):
		names = [name for name in nodes]
		self.nodes = nodes
		self.ring = HashRing(names)
		self.sdbs = {}
		for addr in nodes.values():
			if addr not in self.sdbs:
				self.sdbs[addr] = Sdb(addr)
			
	def close(self):
		for sdb in self.sdbs.values():
			sdb.close()
	
	def put(self, k, v):
		return self.getsdb(k).put(k, v)

	def get(self, k):
		return self.getsdb(k).get(k)
	
	def getsdb(self, k):
		name = self.ring.get_node(k)
		addr = self.nodes[name]
		return self.sdbs[addr]

