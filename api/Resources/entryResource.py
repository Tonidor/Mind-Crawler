import falcon
from sqlalchemy import exists
import uuid

from models import Entry


class EntryResource(object):

    def on_get(self, req, resp):
        try:
            entries = Entry.all()
            if entries:
                resp.status = falcon.HTTP_200
                resp.json = [entry.as_dict for entry in entries]
            else:
                resp.status = falcon.HTTP_404
                resp.json = {"error": "No entries found"}
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

                path_name = "extra/{}.txt".format(str(uuid.uuid4()))
                with open(path_name, "w") as out:
                    out.write(req.get_json('text', dtype=str))
                b.text_path = path_name
                b.save(self.session)
                resp.status = falcon.HTTP_201
                resp.json = {"successfully saved"}
            else:
                resp.status = falcon.HTTP_403
                resp.json = {"error": "Entry already exists"}
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
