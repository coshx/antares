"""Handles requests to build decision trees from a CSV."""
from io import StringIO
import uuid
import pandas as pd
import sklearn.tree
from sklearn.model_selection import train_test_split
import tornado.web
from neo4j.v1 import GraphDatabase


DRIVER = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))


# pylint: disable=W0223
class CSVHandler(tornado.web.RequestHandler):
    """Handles all CRUD operations on CSVs."""

    # pylint: disable=W0221
    def post(self):
        """Parses CSV to dataframe and stores decision tree to Neo4j."""
        csv_data = self.request.files["csv"][0]
        data = pd.read_csv(
            StringIO(str(csv_data["body"], 'utf-8')))
        # pylint: disable=W0612
        train, test = train_test_split(data, test_size=.6)

        tree_model = create_tree_model(train)
        graphviz = sklearn.tree.export_graphviz(tree_model)
        graphviz_lines = graphviz.split('\n')
        java_types = map_java_datatypes(train)
        create_graph(graphviz_lines, java_types)


def map_java_datatypes(df):  # pylint: disable=C0103
    """Maps Python dtypes for all columns in datafrae to Java types."""
    colnames = df.columns.tolist()  # assumes string header
    datatype_map = {
        'u': 'int',
        'i': 'int',
        'b': 'boolean',
        'f': 'double',
        'O': 'String'}
    datatypes = [datatype_map[d.kind] for d in df.dtypes.tolist()]
    return [colnames, datatypes]


def create_tree_model(data):
    """Creates a decision tree classifier from training data."""
    clf = sklearn.tree.DecisionTreeClassifier()
    x, y = data.iloc[:, :-1], data.iloc[:, -1]  # pylint: disable=C0103
    clf = clf.fit(x, y)
    return clf


def create_graph(data, java_types):
    """Writes decision tree to Neo4j using graphviz output."""
    tree_id = str(uuid.uuid4())
    for line in data:
        if line[0].isdigit() and "->" not in line:
            parse_node(line, tree_id, java_types)
        elif line[0].isdigit() and "->" in line:
            node_ids = [int(s) for s in line.split() if s.isdigit()]
            print(node_ids)
            with DRIVER.session() as session:
                new_relationship = "IS_TRUE"
                result = session.write_transaction(
                    check_if_relationship_exists,
                    node_ids[0], tree_id, "IS_TRUE")
                if result is True:
                    new_relationship = "IS_FALSE"
                session.write_transaction(
                    create_relationships, node_ids[0], node_ids[1], tree_id,
                    new_relationship)


def parse_node(line, tree_id, java_types):
    """Parses all graphviz nodes."""
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
        elif '>' in attr or '<' in attr or '=' in attr:
            expression = attr

    with DRIVER.session() as session:
        if expression and node_id == 0:
            session.write_transaction(
                create_root_node, node_id, tree_id, expression, gini, samples,
                java_types, values)
        elif expression:
            session.write_transaction(
                create_rule_node, node_id, tree_id, expression, gini, samples,
                values)
        else:
            session.write_transaction(
                create_leaf_node, node_id, tree_id, gini, samples, values)


# pylint: disable=R0913
def create_rule_node(
        txn, identifier, tree_id, expression, gini, samples, value):
    """Creates a tree node with a classification rule."""
    query = """
    merge (a:Rule {identifier: $identifier,
                   tree_id: $tree_id,
                   expression: $expression,
                   gini: $gini,
                   samples: $samples,
                   value: $value})
    """
    txn.run(
        query,
        identifier=identifier,
        tree_id=tree_id,
        expression=expression,
        gini=gini,
        samples=samples,
        value=value)


def create_leaf_node(txn, identifier, tree_id, gini, samples, value):
    """Creates a tree node with a classification."""
    query = """
    MERGE (a:Answer {identifier: $identifier,
                     tree_id: $tree_id,
                     gini: $gini,
                     samples: $samples,
                     value: $value})
    """
    txn.run(
        query,
        identifier=identifier,
        tree_id=tree_id,
        gini=gini,
        samples=samples,
        value=value)


# pylint: disable=R0913
def create_root_node(
        txn, identifier, tree_id, expression, gini, samples,
        java_types, value):
    """Creates the root node of a tree."""
    parameter_names = ','.join(java_types[0])
    parameter_types = ','.join(java_types[1])
    query = """
    MERGE (a:Rule:Root {identifier: $identifier,
                        tree_id: $tree_id,
                        expression: $expression,
                        gini: $gini,
                        samples: $samples,
                        parameter_names: $parameter_names,
                        parameter_types: $parameter_types,
                        value: $value})
    """
    txn.run(
        query,
        identifier=identifier,
        tree_id=tree_id,
        expression=expression,
        gini=gini,
        samples=samples,
        parameter_names=parameter_names,
        parameter_types=parameter_types,
        value=value)


def create_relationships(
        txn, parent_node_id, child_node_id, tree_id, relationship=None):
    """Creates a TRUE or FALSE relationship between tree nodes."""
    relationship = relationship.upper()
    query = """
    MATCH (a),(b)
    WHERE a.identifier = {parent_node_id} AND
          b.identifier = {child_node_id} AND
          a.tree_id = "{tree_id}" AND
          b.tree_id = "{tree_id}"
    CREATE (a)-[r:{relationship}]->(b)
    """.format(parent_node_id=parent_node_id,
               child_node_id=child_node_id,
               tree_id=tree_id,
               relationship=relationship)
    txn.run(query)


def check_if_relationship_exists(txn, parent_node_id, tree_id, relationship):
    """Checks for existing relationships between nodes."""
    query = """
    MATCH (a) 
    WHERE a.identifier = {parent_node_id} AND 
          a.tree_id = "{tree_id}" AND
          (a)-[:{relationship}]->()
    RETURN a
    """.format(parent_node_id=parent_node_id,
               relationship=relationship,
               tree_id=tree_id)
    result = txn.run(query)
    if result.value():
        return True
    return False
