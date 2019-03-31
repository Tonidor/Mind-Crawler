import falcon

class GraphResource:

    def get_word_vec(self, text):



    def on_get(self, req, resp):
        try:
            text_id = req.get_json('id', dtype=int)
            entry = self.session.query(Entry).get(id)
            if entry is not None:
                with open(entry.path, 'r', encoding='utf-8') as output:

                    resp.json = graph
                    resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': "Box with id {} doesn't exist".format(kit_id)}
        except falcon.HTTPBadRequest as e:
            resp.status = falcon.HTTP_400
            resp.media = {'error': e.description}

    def on_post(self, req, resp):
        try:
            serial = req.get_json('serial', dtype= str, max=16 )
            # If kit already exists
            if not self.session.query(exists().where(Kit.serial == serial)).scalar():
                b = Kit(serial)
                b.save(self.session)
                resp.json = b.as_dict
                resp.status = falcon.HTTP_201
            else:
                resp.status = falcon.HTTP_403
                resp.json = {"error": "Box already exists"}
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
        except Exception as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}