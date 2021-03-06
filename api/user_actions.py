"""Repeatable user actions involving Neo4J"""
from neo4j.v1 import GraphDatabase

DRIVER = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))


def get_user(txn, email):
    """Gets user node."""
    query = """
    MATCH (a:User)
    WHERE a.email = "{email}"
    RETURN a
    """.format(email=email)
    result = txn.run(query)
    return result.value()


def create_user(txn, email, password):
    """Creates a user node."""
    query = """
    MERGE (a:User {email: $email,
                password: $password})
    """
    return txn.run(
        query,
        email=email,
        password=password)


def user_exists(email):
    """Checks if user exists"""
    with DRIVER.session() as session:
        return bool(session.read_transaction(
            get_user, email))
