class File(object):
    
    def __init__(
        self,
        file_name
    ):
        self.file_name = file_name


    def open(
        self,
        url
    ):
        return 200, open(self.file_name, "r").read()
