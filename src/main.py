
import sys
import json
from SearchAndReplace import SearchReplace


def read_arguments():
    # read arguments
    number_args = len(sys.argv)
    if number_args != 3:
        print("invalid arguments")
    return [sys.argv[1], sys.argv[2]]


def read_search_replace_config(search_replace_config_file):
    return json.load(open(search_replace_config_file, 'r'))


def main():
    in_file, search_replace_config_file = read_arguments()
    search_replace_processor = SearchReplace(open(in_file,'r'), open('out', 'w'),
                                                read_search_replace_config(search_replace_config_file), 5000)
    search_replace_processor.run()

if __name__ == "__main__":
    main()

