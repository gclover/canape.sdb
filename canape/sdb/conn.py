
import gevent
from gevent import socket
from canape.sdb import gutils

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
			if ha != 'error':
				return res
		except Exception, e:
			print e	

	def get(self, k):
		try:
			(ha, res) = gutils.sendrecv(self.sock, 'get', k)
			if ha != 'error':
				return res
		except Exception, e:
			print e
		
class ClusterSdb(object):
	
	import ring_;

	def __init__(self, nodes):
		self.ring = ring_.Ring();
		self.nodes = {}
		for (name, addr) in enumerate(nodes):
			self.nodes[name] = Sdb(addr)
			self.ring.addnode(name)

	def close(self):
		for sdb in self.nodes.values():
			sdb.close()
	
	def put(self, k, v)
		return self.nodes[self.ring.getnode(k)].put(k, v)

	def get(self, k)
		return self.nodes[self.ring.getnode(k)].get(k)

