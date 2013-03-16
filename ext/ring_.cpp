#include "ring_.h"

using namespace ring;

Ring_::Ring_()
: ring_(4, StrHash())
{}

Ring_::~Ring_()
{}

void Ring_::addnode(std::string node)
{
	ring_.AddNode(node);		
}

std::string Ring_::getnode(std::string key)
{
	return ring_.GetNode(key);
}


