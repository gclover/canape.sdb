# distutils: language = c++
# distutils: sources = ext/ring_.cpp

from libcpp.string cimport string
from libcpp cimport bool

cdef extern from "ring_.h" namespace "ring":
	cdef cppclass Ring_:
		Ring_() except + 
		void addnode(string)
		string getnode(string)

cdef class Ring:
	cdef Ring_ *thisptr
	def __cinit__(self):
		self.thisptr = new Ring_()
	def __dealloc__(self):
		del self.thisptr

	def addnode(self, node):
		self.thisptr.addnode(node)

	def getnode(self, key):
		return self.thisptr.getnode(key)

