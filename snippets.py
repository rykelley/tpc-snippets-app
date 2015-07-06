__author__ = 'Ryan'


import logging
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)


def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet...

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # building put parser
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help=" Stores Name")
    put_parser.add_argument("snippets", help=" Stores the snippet of text")

    # building get parser
    logging.debug("Building get Subparser")
    get_parser = subparsers.add_parser("get", help="Gets Name")
    get_parser.add_argument("name", help="Gets name")

    arguments = parser.parse_args(sys.argv[1:])
    # convert passed arguments from namespaces to dictionary
    arguments = var(arguments)
    command = arguments.pop("Command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r}} to {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved {!r}".format(snippet))


if __name__ == "__main__":
    main()
