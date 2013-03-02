from google.appengine.api import memcache, files, images, urlfetch
import hashlib, datetime, logging


def format_number(value):
    return "{:,.0f}".format(value).replace(',','.')

def create_key_name(input):
	return hashlib.sha224(input.encode('utf-8') + str(datetime.datetime.now())).hexdigest()

def set_memcache_object(key, item):
	memcache.set(key, item, 86400)
	
def get_memcache_object(kn):
	return memcache.get(kn)

def get_memcache_objects(keys):
	return memcache.get_multi(keys)