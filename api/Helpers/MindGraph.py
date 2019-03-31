from colour import Color
from numpy import linalg as LAG


class Node:
    def __init__(self, topic_centroid, position, word, occurrence):
        self.color = topic_centroid.calculate_color_interpolation(position)
        self.word = word
        self.position = position
        self.occurrences = 0

    @@property
    def radius(self):
        return (self.occurrences / 10) + 5


    def __repr__(self):
        return str({"word": self.word, "color": self.color, "radius": self.radius})

    def add_occurences(self, times = 1):
        self.occurrences += times

class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str({"source": repr(self.source), "target": repr(self.target), "weight": self.weight})


class MindGraph:
    def __init__(self):
        self.words_used = set()
        self.nodes = {}

    def get_or_create_node(self, word, ):
        if word in self.words_used:
            self.nodes.get(word)
        else:
            n = Node(word)
            self.nodes[word] = n
            return n


colors = [
    Color("red"),
    Color("blue"),
    Color("yellow"),
    Color("green"),
    Color("orange"),
    Color("purple"),
]


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