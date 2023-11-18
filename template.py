import argparse

parser = argparse.ArgumentParser(description='Creates templates for various programming languages and projects.')
parser.add_argument("input", metavar="type", nargs=1, help='Type of the template')
parser.add_argument("input", metavar="name", nargs=1, help='Name of the template')
parser.add_argument("-l", "--list", action="store_true", default=False, help="Lists the different templates available.")
args = parser.parse_args()
