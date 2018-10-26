import numpy as np
from sklearn import tree

def split_train_test(data, percent_train=0.6):
    split_index = round(np.shape(data)[0] * percent_train)
    np.random.shuffle(data)
    train, test = data[:split_index], data[split_index:]
    return train, test

def create_tree_model(data, max_depth):
    clf = tree.DecisionTreeClassifier()
    x, y = data[:,:-1], data[:,-1]
    clf = clf.fit(x, y)
    return clf
