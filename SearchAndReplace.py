
from Trie import Trie

class SearchReplace:
    __in = None
    __out = None
    __map = None
    __Trie = None
    __read_size = None

    def __init__(self, in_fd, out_fd, search_replace_map, buffer_size = 2048):
        self.__in = in_fd
        self.__out = out_fd
        self.__map = search_replace_map
        self.__Trie = Trie(search_replace_map)
        self.__read_size = buffer_size
        self.__Trie.reset()

    def read_data(self):
        return self.__in.read(self.__read_size)

    def write_data(self, processed_data, _len):
        for lst_iter in range(_len):
            self.__out.write(processed_data[lst_iter])

    def run(self):
        partially_matched_str = []
        while True:
            curr_data = self.read_data()
            if len(curr_data) == 0:
                break
            for ch in curr_data:
                partially_matched_str.append(ch)
                suffix_matching_len, suffix_search_str_matching_len, replace_str = self.__Trie.move_next(ch)
                if suffix_search_str_matching_len:
                    unmatching_len = len(partially_matched_str) - suffix_search_str_matching_len
                    self.write_data(partially_matched_str, unmatching_len)
                    self.write_data(replace_str, len(replace_str))
                    partially_matched_str.clear()
                    self.__Trie.reset()
                else:
                    unmatching_len = len(partially_matched_str) - suffix_matching_len
                    self.write_data(partially_matched_str, unmatching_len)
                    for _ in range(unmatching_len):
                        partially_matched_str.pop(0)

        self.write_data(partially_matched_str, len(partially_matched_str))
        partially_matched_str.clear()


if __name__ == '__main__':
    _in = open('in')
    _out = open('out', 'w')
    _search_replace_map = {'aaa': 'def', 'aba': ' ', 'ba': 'wsc'}
    txt_process = SearchReplace(_in, _out, _search_replace_map)
    txt_process.run()
