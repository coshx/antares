import json
import numpy as np
import pickle
import redis
from sklearn.datasets import load_iris
import sklearn.tree
import tornado.web
import uuid

redis = redis.Redis(
    host='localhost',
    port=6379,
    password='')

class CSVHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.get_argument("csv")
        # TODO: Parse data from frontend
        iris = load_iris()
        data = np.hstack((iris.data, np.reshape(iris.target, (-1, 1))))
        train, test = split_train_test(data, .6)

        ids = []
        response = {}
        model_types = [("simple", 2), ("complex", 3), ("highly_complex", 4)]
        for model_type, max_depth in model_types:
            tree_model = create_tree_model(train, max_depth)
            tree_object = {"tree": tree_model, "model_type": model_type, "accuracy": 100}
            tree_id = uuid.uuid1()
            redis.set(tree_id, pickle.dumps(tree_object))
            ids.append(tree_id)
            response[model_type] = str(tree_id)
        self.write(json.dumps(response))


def split_train_test(data, percent_train=0.6):
    split_index = round(np.shape(data)[0] * percent_train)
    np.random.shuffle(data)
    train, test = data[:split_index], data[split_index:]
    return train, test

def create_tree_model(data, max_depth):
    clf = sklearn.tree.DecisionTreeClassifier()
    x, y = data[:,:-1], data[:,-1]
    clf = clf.fit(x, y)
    return clf

def test_split_train_test():
    data = np.zeros((67, 4))
    train, test = split_train_test(data)
    assert np.shape(train) == (40, 4)
    assert np.shape(test) == (27, 4)
