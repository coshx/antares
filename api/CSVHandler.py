import numpy as np
from sklearn.datasets import load_iris
from neo4j.v1 import GraphDatabase
import sklearn.tree
import tornado.web
import pandas as pd
from io import StringIO


DRIVER = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))


class CSVHandler(tornado.web.RequestHandler):

    def post(self):
        csv_data = self.request.files["csv"][0]
        panda_store = pd.read_csv(StringIO(str(csv_data["body"], 'utf-8')))
        import pdb; pdb.set_trace()
        # TODO: Parse data from frontend
        iris = load_iris()
        data = np.hstack((iris.data, np.reshape(iris.target, (-1, 1))))
        train, test = split_train_test(data, .6)

        #model_types = [("simple", 2), ("complex", 3), ("highly_complex", 4)]
        #for model_type, max_depth in model_types:
        
        tree_model = create_tree_model(train, 5)
        graphviz = sklearn.tree.export_graphviz(tree_model)
        graphviz_lines = graphviz.split('\n')
        create_graph(graphviz_lines)


def split_train_test(data, percent_train=0.6):
    split_index = round(np.shape(data)[0] * percent_train)
    np.random.shuffle(data)
    train, test = data[:split_index], data[split_index:]
    return train, test


def create_tree_model(data, max_depth):
    clf = sklearn.tree.DecisionTreeClassifier()
    x, y = data[:, :-1], data[:, -1]
    clf = clf.fit(x, y)
    return clf


def test_split_train_test():
    data = np.zeros((67, 4))
    train, test = split_train_test(data)
    assert np.shape(train) == (40, 4)
    assert np.shape(test) == (27, 4)


def create_graph(data):
    for line in data:
        if (line[0].isdigit()) and ("->" not in line):
            parse_node(line)
        elif (line[0].isdigit()) and ("->" in line):
            node_ids = [int(s) for s in line.split() if s.isdigit()]
            print(node_ids)
            with DRIVER.session() as session:
                new_relationship = "IS_TRUE"
                result = session.write_transaction(
                    check_if_relationship_exists, node_ids[0], "IS_TRUE")
                if(result == True):
                    new_relationship = "IS_FALSE"
                session.write_transaction(
                    create_relationships, node_ids[0], node_ids[1], new_relationship)
        
def parse_node(line):
    node = line.split("\"")[1].split("\\n")
    node_id = int(line.split(" ")[0])
    expression = ""
    for attr in node:
        if 'gini' in attr:
            gini = float(attr.strip().split(" ")[-1])
        elif 'samples' in attr:
            samples = float(attr.strip().split(" ")[-1])
        elif 'value' in attr:
            values = attr.strip().split(
                "[")[-1].replace("]", "").replace(" ", "").split(",")
            values = [int(v) for v in values]
        else:
            expression = attr

    with DRIVER.session() as session:
        if expression and node_id == 0:
            session.write_transaction(
                create_root_node, node_id, expression, gini, samples, values)
        elif expression:
            session.write_transaction(
                create_rule_node, node_id, expression, gini, samples, values)
        else:
            session.write_transaction(
                create_leaf_node, node_id, gini, samples, values)

def create_rule_node(tx, identifier, expression, gini, samples, value):
    tx.run(
        "MERGE (a:Rule {identifier: $identifier, expression: $expression, gini: $gini, samples: $samples, value: $value}) ",
        identifier=identifier,
        expression=expression,
        gini=gini,
        samples=samples,
        value=value)


def create_leaf_node(tx, identifier, gini, samples, value):
    tx.run(
        "MERGE (a:Answer {identifier: $identifier, gini: $gini, samples: $samples, value: $value}) ",
        identifier=identifier,
        gini=gini,
        samples=samples,
        value=value)

def create_root_node(tx, identifier, expression, gini, samples, value):
    tx.run(
        "MERGE (a:Rule:Root {identifier: $identifier, expression: $expression, gini: $gini, samples: $samples, value: $value}) ",
        identifier=identifier,
        expression=expression,
        gini=gini,
        samples=samples,
        value=value)

def create_relationships(
        tx,
        parent_node_identifier,
        child_node_identifier,
        relationship=None):
    relationship = relationship.upper()
    query = '''
    MATCH (a),(b)
    WHERE a.identifier = {parent_node_identifier} AND b.identifier = {child_node_identifier}
    CREATE (a)-[r:{relationship}]->(b)
    '''.format(parent_node_identifier=parent_node_identifier,
               child_node_identifier=child_node_identifier,
               relationship=relationship)
    tx.run(query)


def check_if_relationship_exists(tx, parent_node_identifier, relationship):
    query = ''' 
    MATCH (a) WHERE a.identifier = {parent_node_identifier} AND (a)-[:{relationship}]->()
    RETURN a
    '''.format(parent_node_identifier=parent_node_identifier, relationship=relationship)
    result = tx.run(query)
    if result.value():
        return True
    return False