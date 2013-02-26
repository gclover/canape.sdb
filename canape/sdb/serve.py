
from gevent.server import StreamServer
from gutils import Processor, SockHandle

import redis
import leveldb

class CacheDb(object):

	def __init__(self, host, port):
		self.db = redis.StrictRedis(host=host, port=port, db=0)			
	
	def get(self, k):
		return self.db.get(k)

	def put(self, k, v):
		return self.db.set(k, v)

class FileDb(object):

	def __init__(self, path):
		self.db = leveldb.LevelDB(path)
	
	def get(self, k):
		return self.db.Get(k)

	def put(self, k, v):
		return self.db.Put(k, v)


class SdbProcessor(Processor):
	
	def __init__(self, cachedb, filedb):
		self.cachedb = cachedb
		self.filedb = filedb

	def get(self, pa):
		k = pa
		v = self.cachedb.get(k)
		if v is not None:
			return v
		v = self.filedb.get(k)
		if v is not None:
			self.cachedb.put(k, v)
			return v

		return None

	def put(self, pa):
		(k, v) = pa
		self.filedb.put(k, v)
		return True


def main():
	
	import sys
	
	cachedb = CacheDb('localhost', 6379)
	filedb = FileDb('/tmp/l2')
	
	processor = SdbProcessor(cachedb, filedb)
	handle = SockHandle(processor)
	server = StreamServer(('0.0.0.0', 6000), handle)
	print 'Starting sdb server on port 6000'
	
	server.serve_forever()
	