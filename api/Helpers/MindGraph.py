from colour import Color
from numpy import linalg as LAG
import gensim.downloader as api
from sklearn import cluster
from sklearn import metrics


colors = [
    Color("red"),
    Color("blue"),
    Color("yellow"),
    Color("green"),
    Color("orange"),
    Color("purple"),
]


class Node:
    def __init__(self, word, centroid, position):
        self.word = word
        self.position = position
        self.topic = centroid.topic
        self.occurrences = 0
        self.color = centroid.calculate_color_interpolation(position)

    @property
    def radius(self):
        return (self.occurrences / 10) + 5

    def __repr__(self):
        return str({"word": self.word, "color": self.color, "radius": self.radius, "group": self.topic})

    def add_occurences(self, times=1):
        self.occurrences += times

    def update_centroid(self, centroid, position):
        self.color = centroid.calculate_color_interpolation(self.position)
        self.position = position
        self.topic = centroid


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
        self.topics_created = set()
        self.centroids = {}
        self.nodes = {}
        self.edges = set()
        self.word2vec = api.load("glove-wiki-gigaword-100")

    def get_or_create_centroid(self, topic, position):
        if topic in self.topics_created:
            return self.centroids.get(topic)
        else:
            t = Centroid(topic, position)
            self.centroids[topic] = t
            self.topics_created.add(topic)
            return t

    def get_or_create_node(self, word, centroid=None, position=None):
        if word in self.words_used:
            return self.nodes.get(word)
        else:
            n = Node(word, centroid, position)
            self.nodes[word] = n
            self.words_used.add(word)
            return n

    def add_edge(self, target, source):
        self.edges.add(Edge(target, source, self.word2vec_distance(target.word, source.word)))

    def word2vec_distance(self, target, source):
        return 1 - self.word2vec.distance(target, source)

    @property
    def as_dict(self):
        return {"nodes": [repr(node) for key, node in self.nodes.items()],
                "edges": [repr(edge) for edge in self.edges]}

    def calc_centroids_and_nodes(self):

        # do kmeans clustering
        kmeans = cluster.KMeans(n_clusters=6)
        kmeans.fit(self.word2vec.vocab)

        # create centroids
        topics = kmeans.labels_
        centroid_positions = kmeans.cluster_centers_
        for topic, centroid_position in zip(topics, centroid_positions):
            self.get_or_create_centroid(topic, centroid_position)

        max_distances = {}
        for word in self.words_used:

            # create node
            w2vpos = self.word2vec[word]
            centroid = kmeans.predict(w2vpos)
            node = self.get_or_create_node(word, centroid, w2vpos)

            # update max_dist for every centroid
            distance = LAG.norm(w2vpos, self.centroids[centroid].position)
            if distance > max_distances[centroid]:
                max_distances[centroid] = distance

            # add node to centroid.nodes
            self.centroids[centroid].nodes.append(node)

        for centroid in self.centroids.values():
            centroid.max_distance = max_distances[centroid.index]

        for centroid in centroid_positions.values():
            for source in centroid.nodes:
                for target in centroid.nodes:
                    if target is not source:
                        self.add_edge(target, source)


class Centroid:
    def __init__(self, topic, position):
        self.topic = topic
        self.position = position
        self.color = colors[topic]
        self.max_distance = 0
        self.nodes = []

    def calculate_color_interpolation(self, target):
        distance = LAG.norm(self.position, target)
        norm_distance = abs(self.max_distance - distance) / self.max_distance
        temp = self.color.get_hsl()
        temp.set_luminance(self.color.get_luminance() * norm_distance)
        return temp
