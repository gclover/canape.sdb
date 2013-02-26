
import msgpack
import struct
import sys
import traceback

def pack(handle, params):
	return msgpack.packb({'ha': handle, 'pa': params})

def unpack(msg):
	req = msgpack.unpackb(msg)
	return (req['ha'], req['pa'])
	
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
	send(sock, '_bye_', '')
	
class SockHandle(object):

	def __init__(self, processor):
		self.processor = processor

	def __call__(self, sock, address):
		try:
			while True:
				(ha, pa) = recv(sock)
				if ha == '_bye_':
					break
				re = self.processor.run(ha, pa)
				if ha.endswith('_'):
					continue
				send(sock, ha, re)
		except Exception, e:
			traceback.print_exc(file=sys.stdout)
			send(sock, 'error', str(e))
		#sock.shutdown(socket.SHUT_WR)
		sock.close()

class Processor(object):

	def run(self, handle, params):
		return getattr(self, handle)(params)


