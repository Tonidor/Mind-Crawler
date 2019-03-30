import falcon
from sqlalchemy import exists

from models import Entry


class EntryResource(object):

    def on_get(self, req, resp):
        try:
            entry_id = req.get_json('id', dtype=int)
            entry = self.session.query(Entry).get(entry_id)
            if entry is not None:
                response = entry.as_dict
                resp.status = falcon.HTTP_200
                resp.media = response
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': "Entry with id {} doesn't exist".format(entry_id)}
        except falcon.HTTPBadRequest as e:
            resp.status = falcon.HTTPBadRequest_400
            resp.media = {'error': e.description}

    def on_post(self, req, resp):
        try:
            text_path = req.get_json('text_path', dtype=str)
            if not self.session.query(exists().where(Entry.text_path == text_path)).scalar():
                b = Entry()
                b.date = req.get_json('date', dtype=int)
                b.title = req.get_json('title', dtype=str)
                b.text_path = req.get_json('text_path', dtype=str)
                b.save(self.session)
                resp.json = b.as_dict
                resp.status = falcon.HTTP_201
            else:
                resp.status = falcon.HTTP_403
                resp.json = {"error": "Entry already exists"}
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
