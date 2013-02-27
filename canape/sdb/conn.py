
import gevent
from gevent import socket
from canpae.sdb import gutils

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
		

	




