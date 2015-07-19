__author__ = 'Ryan'

import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='root' host='104.131.148.235'")
logging.debug("Database connection established.")


def put(name, snippet):
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    try:
        command = "insert into snippets VALUES (%s,%s)"
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))
        connection.commit()
        logging.debug("Snippets stored")
        return name, snippet


def get(name):
    logging.info("grabbing snippet {!r}".format(name,))
    cursor = connection.cursor()
    command = "select message from snippets where keyword = (%s)"
    cursor.execute(command, (name,))
    fetch = cursor.fetchone()
    logging.debug("Fetched it")
    return fetch[0]


def catalog():
    """Query the available keywords from the snippets table."""
    logging.info("Querying the database")
    with connection.cursor() as cursor:
        cursor.execute(
            "select keyword from snippets order by keyword ASC")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
    logging.debug("Query complete")


def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # building put parser
    logging.debug("Constructing put sub-parser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help=" Stores Name")
    put_parser.add_argument("snippet", help=" Stores the snippet of text")

    # building get parser
    logging.debug("Building get sub-parser")
    get_parser = subparsers.add_parser("get", help="Gets Name")
    get_parser.add_argument("name", help="Gets name")

    # building the catalog parser
    logging.debug("Building the catalog sub-parser")
    catalog_parser = subparsers.add_parser("catalog", help="catalogs some stuff")
    catalog_parser.add_argument("catalog", help="catalogs some stuff")

    arguments = parser.parse_args(sys.argv[1:])
    # convert passed arguments from namespaces to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} to {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved {!r}".format(snippet))
    elif command == "catalog":
        catalog()
        print("retrieved keywords")


if __name__ == "__main__":
    main()
