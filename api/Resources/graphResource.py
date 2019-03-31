import falcon
from Helpers import MindGraph
from models import Entry
from itertools import chain


class GraphResource:
    def __init__(self):
        self.mg = MindGraph()

    def createWordList(self,line):
        wordList2 = []
        wordList1 = line.split()
        for word in wordList1:
            cleanWord = ""
            for char in word:
                if char in '!,.?":;0123456789':
                    char = ""
                cleanWord += char
            wordList2.append(cleanWord)
        return wordList2

    def on_get(self, req, resp):
            entries = Entry.all()
            docs = [entry.text for entry in entries]
            del entries
            huge_ass_doc = []
            for entry in docs:
                huge_ass_doc.append(self.createWordList(entry))

            corpus = list(chain.from_iterable(huge_ass_doc))

            for word in corpus:
                self.mg.get_or_create_node(word)

            self.mg.calc_centroids_and_nodes()

            resp.json = self.mg.as_dict