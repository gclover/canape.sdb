
from gevent import socket
import msgpack
import struct
import sys
import traceback

handle_tag = 'HA'
params_tag = 'PA'
bye_tag = '_BYE_'

def pack(handle, params):
	return msgpack.packb({handle_tag: handle, params_tag: params})

def unpack(msg):
	req = msgpack.unpackb(msg)
	return (req[handle_tag], req[params_tag])
	
def send(sock, ha, pa):
	req = pack(ha, pa)
	head = struct.pack('I', len(req))
	sock.send(head + req)

def recv(sock):
	head = sock.recv(4)
	(le,) = struct.unpack('I', head)
	req = sock.recv(le)
	(ha, pa) = unpack(req)
	return (ha, pa)

def sendrecv(sock, ha, pa):
	send(sock, ha, pa)
	return recv(sock)

def bye(sock):
	send(sock, bye_tag, '')
	
class SockHandle(object):

	def __init__(self, processor):
		self.processor = processor

	def __call__(self, sock, address):
		try:
			while True:
				(ha, pa) = recv(sock)
				if ha == bye_tag:
					break
				hap = ha[0:-1] if ha.endswith('_') else ha
				re = self.processor.run(hap, pa)
				if ha.endswith('_'):
					continue
				send(sock, 0, re)
		except Exception, e:
			traceback.print_exc(file=sys.stdout)
			send(sock, -1, str(e))
		sock.close()

class Processor(object):

	def run(self, handle, params):
		return getattr(self, handle)(params)


