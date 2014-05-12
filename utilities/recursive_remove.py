#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**recursive_remove.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Recursion delete.

**Others:**

"""

from __future__ import unicode_literals

import argparse
import os
import sys

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["recursive_remove", "remove", "get_command_line_arguments", "main"]


def recursive_remove(root_directory, pattern):
    """
    Recursively deletes the matching items.

    :param root_directory: Directory to recurse.
    :type root_directory: unicode
    :param pattern: Pattern to match.
    :type pattern: unicode
    """

    if not os.path.exists(root_directory):
        return

    for root, dirs, files in os.walk(root_directory, followlinks=True):
        for item in files:
            item_path = os.path.join(root, item).replace("\\", "/")
            if pattern in item:
                remove(item_path)


def remove(item):
    """
    Deletes given item.
    :param item: Item to delete.
    :type item: unicode
    """

    print("{0} | Removing file: '{1}'".format(remove.__name__, item))
    try:
        os.remove(item)
    except:
        print("{0} | '{1}' file removing failed!".format(remove.__name__, item))


def get_command_line_arguments():
    """
    Retrieves command line arguments.

    :return: Namespace.
    :rtype: Namespace
    """

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-h",
                        "--help",
                        action="help",
                        help="'Displays this help message and exit.'")

    parser.add_argument("-i",
                        "--input",
                        type=unicode,
                        dest="input",
                        help="'Input directory to recurse.'")

    parser.add_argument("-p",
                        "--pattern",
                        type=unicode,
                        dest="pattern",
                        help="'Pattern to match.'")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    """
    Starts the Application.

    :return: Definition success.
    :rtype: bool
    """

    args = get_command_line_arguments()
    return 0 if recursive_remove(args.input, args.pattern) else 1


if __name__ == "__main__":
    main()
