import falcon
from model import Entry
class GraphResource:
    def on_get(self, req, resp):
            entries = Entry.all()

            
