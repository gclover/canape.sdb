
from gevent.server import StreamServer
from gutils import Processor, SockHandle

import redis
import leveldb

class CacheDb(object):

	def __init__(self, addr):
		if type(addr) is tuple:
			# tcp socket
			(host, port) = addr
			self.db = redis.Redis(host=host, port=port, db=0)			
		else:
			# unix domain socket
			sockfile = addr
			self.db = redis.Redis(unix_socket_path=sockfile)			
	
	def get(self, k):
		return self.db.get(k)

	def put(self, k, v):
		return self.db.set(k, v)

class StorageDb(object):

	def __init__(self, path):
		self.db = leveldb.LevelDB(path)
	
	def get(self, k):
		return self.db.get(k)

	def put(self, k, v):
		return self.db.put(k, v)


class SdbProcessor(Processor):
	
	def __init__(self, cachedb, storagedb):
		self.cachedb = cachedb
		self.storagedb = storagedb

	def get(self, pa):
		k = pa
		v = self.cachedb.get(k)
		if v is not None:
			return v
		v = self.storagedb.get(k)
		if v is not None:
			self.cachedb.put(k, v)
		return v

	def put(self, pa):
		(k, v) = pa
		return self.storagedb.put(k, v)

def serve():
	
	from optparse import OptionParser
	
	parser = OptionParser()
	parser.add_option('-c', '--cache', dest='cache_addr', help='cache address')
	parser.add_option('-s', '--storage', dest='storage_addr', help='storage file address')
	(options, args) = parser.parse_args()
	
	storage_addr = options.storage_addr
	cache_addr = options.cache_addr
	if ':' in cache_addr:
		(host, port) = (cache_addr.split(':'))
		port = int(port)
		cache_addr = (host, port)
	
	cachedb = CacheDb(cache_addr)
	filedb = StorageDb(storage_addr)
	
	processor = SdbProcessor(cachedb, filedb)
	handle = SockHandle(processor)
	server = StreamServer(('0.0.0.0', 6000), handle)
	print 'Starting sdb server on port 6000'
	
	server.serve_forever()
	

	
