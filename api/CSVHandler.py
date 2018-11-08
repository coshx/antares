import json
import numpy as np
import pickle
from sklearn.datasets import load_iris
from neo4j.v1 import GraphDatabase
import sklearn.tree
import tornado.web
import uuid

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

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
            graphviz = sklearn.tree.export_graphviz(tree_model)

            graphviz_lines = graphviz.split('\n')
            create_graph_nodes(graphviz_lines)

            # for line in graphviz_lines:
            #     if (line[0].isdigit()) and ("->" in line):
            #         with driver.session() as session:
            #             #create relationships


        # self.write(json.dumps(tree_object))


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

def create_graph_nodes(data):
    for line in data:
        if (line[0].isdigit()) and ("->" not in line):
            node = line.split("\"")[1].split("\\n")
            node_id = int(line[0])
            gini = ""
            samples = ""
            values = ""
            expression = ""
            for attr in node:
                if 'gini' in attr:
                    gini = float(attr.split(" ")[-1])
                elif 'samples' in attr:
                    samples = float(attr.split(" ")[-1])
                elif 'value' in attr:
                    values = attr.split("[")[-1].replace("]", "").replace(" ", "").split(",")
                    values = list(map(int, values))
                else:
                    expression = attr
            
            with driver.session() as session:
                if expression:
                    session.write_transaction(create_rule_node, node_id, expression, gini, samples, values)
                else:
                    session.write_transaction(create_leaf_node, node_id, gini, samples, values)

def create_rule_node(tx, identifier, expression, gini, samples, value):
    tx.run("MERGE (a:Rule {identifier: $identifier, expression: $expression, gini: $gini, samples: $samples, value: $value}) ",
           identifier=identifier, expression=expression, gini=gini, samples=samples, value=value)

def create_leaf_node(tx, identifier, gini, samples, value):
    tx.run("MERGE (a:Answer {identifier: $identifier, gini: $gini, samples: $samples, value: $value}) ",
           identifier=identifier, gini=gini, samples=samples, value=value)

def create_relationships(tx, parent_node_identifier, child_node_identifier, relationship):
    relationship = relationship.upper()
    tx.run("MATCH (a),(b)"
           "WHERE a.identifier = $parent_node_identifier AND b.identifier = $child_node_identifier"
           "CREATE (a)-[r:$relationship]->(b)",
           parent_node_identifier=parent_node_identifier, child_node_identifier=child_node_identifier, relationship=relationship)
