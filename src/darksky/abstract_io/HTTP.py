import requests

class HTTP(object):

    def __init__ (
        self,
        get = None
    ):
        self.get = get or requests.get

    
    def open(self, url):
        request = self.get(url)
        return request.status_code, request.text
