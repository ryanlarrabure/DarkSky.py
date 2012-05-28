import urllib2

class HTTP(object):

    def __init__ (
        self,
        urllib2_mod = None
    ):
        self.urllib2 = urllib2_mod or urllib2

    
    def open(self, url):
        request = self.urllib2.urlopen(url)
        return request.getcode(), request.read()
