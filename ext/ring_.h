#ifndef RING__H
#define RING__H

#include <map>
#include <string>
#include <iostream>

#include "consistent.h"

namespace ring 
{

struct StrHash
{
	size_t operator()(const char * str) const
	{
		size_t hash = 0;
		int c;

		while ((c = *str++)) {
			hash = c + (hash << 6) + (hash << 16) - hash;
		}

		return hash;
	}
};

class Ring_
{
public:
	Ring_();
	~Ring_();
	void addnode(std::string node);
	std::string getnode(std::string key);
private:
        Consistent::HashRing<std::string, std::string, StrHash> ring_;
};

}


#endif
