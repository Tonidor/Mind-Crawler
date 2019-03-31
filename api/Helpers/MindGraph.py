from colour import Color
from numpy import linalg as LAG
import gensim
import gensim.downloader as api


colors = [
    Color("red"),
    Color("blue"),
    Color("yellow"),
    Color("green"),
    Color("orange"),
    Color("purple"),
]


class Node:
    def __init__(self, topic_centroid, position, word):
        self.color = topic_centroid.calculate_color_interpolation(position)
        self.word = word
        self.position = position
        self.occurrences = 0
        self.group = topic_centroid.topic_index

    @property
    def radius(self):
        return (self.occurrences / 10) + 5

    def __repr__(self):
        return str({"word": self.word, "color": self.color, "radius": self.radius, "group": self.group})

    def add_occurences(self, times = 1):
        self.occurrences += times


class Edge:
    def __init__(self, source, target, thickness):
        self.source = source
        self.target = target
        self.thickness = thickness

    def __repr__(self):
        return str({"source": self.source.word, "target": self.target.word, "weight": self.thickness})


class MindGraph:
    def __init__(self):
        self.words_used = set()
        self.nodes = {}
        self.edges = set()
        self.word2vec = api.load("glove-wiki-gigaword-100")

    def get_or_create_node(self, word, topic_centroid, position):
        if word in self.words_used:
            return self.nodes.get(word)
        else:
            n = Node(topic_centroid,position, word)
            self.nodes[word] = n
            self.words_used.add(word)
            return n

    def add_edge(self, target, source):
        self.edges.add((target, source, self.word2vec_distance(target.word, source.word)))

    def word2vec_distance(self, target, source):
        return 1 - self.word2vec.distance(target, source)

    @property
    def as_dict(self):
        return {"nodes": [repr(node) for key, node in self.nodes.items()],
                "edges": [repr(edge) for edge in self.edges]}


class TopicCentroid:
    def __init__(self, topic_index, position, max_distance):
        self.color = colors[topic_index]
        self.position = position
        self.max_distance = max_distance

    def calculate_color_interpolation(self, target):
        distance = LAG.norm(self.position, target)
        norm_distance = (self.max_distance - distance) / self.max_distance
        temp = self.color.get_hsl()
        temp.set_luminance(self.color.get_luminance() * norm_distance)
        return temp