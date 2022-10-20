class TrieNode:
    __ch = None
    __depth = None
    __replaceStr = None

    def find_max_suffix_equal_to_prefix(self, prev_node):
        if prev_node is None:
            return

        if prev_node.is_head():
            self.max_suffix_equal_to_prefix = prev_node
            return

        curr_ch = self.__ch
        iter_node = prev_node.max_suffix_equal_to_prefix
        while iter_node.has_next_ch(curr_ch) is False and iter_node.is_head() is False:
            iter_node = iter_node.max_suffix_equal_to_prefix

        if iter_node.has_next_ch(curr_ch):
            self.max_suffix_equal_to_prefix = iter_node.get_next_ch(curr_ch)
        else:
            self.max_suffix_equal_to_prefix = iter_node

    def find_max_suffix_equal_to_search_str(self):
        if self.is_end_of_search_str() == False:
            self.max_suffix_equal_to_search_str = self.max_suffix_equal_to_prefix.max_suffix_equal_to_search_str

    def __int__(self):
        pass

    def __init__(self, ch, depth):
        self.__ch = ch
        self.nextCh = {}
        self.__depth = depth
        self.max_suffix_equal_to_prefix = self
        self.max_suffix_equal_to_search_str = self

    def __str__(self):
        lst = list()
        lst.append(self)
        lst.append(self.__ch)
        lst.append(self.nextCh)
        lst.append(self.__depth)
        lst.append(self.__replaceStr)
        lst.append(self.max_suffix_equal_to_prefix)
        lst.append(self.max_suffix_equal_to_search_str)
        return lst.__str__()

    def is_head(self):
        if self.max_suffix_equal_to_prefix == self:
            return True
        return False

    def print_rec(self):
        print(self.__str__())
        for ch_node in self.nextCh.items():
            ch_node[1].print_rec()

    def mark_end_of_search_str(self, replace_str):
        self.__replaceStr = replace_str

    def insert_next_ch(self, next_ch):
        child_map = self.nextCh
        if child_map.get(next_ch) is None:
            next_trie_node = TrieNode(next_ch, self.__depth+1)
            child_map[next_ch] = next_trie_node
        return child_map[next_ch]

    def has_next_ch(self, next_ch):
        if self.nextCh.get(next_ch) is None:
            return False
        return True

    def get_next_ch(self, next_ch):
        return self.nextCh.get(next_ch)

    def get_depth(self):
        return self.__depth

    def is_end_of_search_str(self):
        if self.__replaceStr is not None:
            return True
        else:
            return False

    def get_replace_str(self):
        return self.__replaceStr


class Trie:
    __head = None
    __curr_trie_node = None

    def __init__(self, search_replace_map):
        self.__head = TrieNode('\0', 0)
        self.__curr_trie_node = self.__head
        search_replace_lst = search_replace_map.items()
        for search_str, replace_str in search_replace_lst:
            node_iter = self.__head
            for ch in search_str:
                node_iter = node_iter.insert_next_ch(ch)
            node_iter.mark_end_of_search_str(replace_str)

        queue = []
        queue.append(self.__head)
        while len(queue):
            curr_node = queue.pop(0)
            for nxt_node in curr_node.nextCh.values():
                nxt_node.find_max_suffix_equal_to_prefix(curr_node)
                nxt_node.find_max_suffix_equal_to_search_str()
                queue.append(nxt_node)

    def print_trie(self):
        self.__head.print_rec()

    # returns the next largest match length and if match found returns the string to be replaced
    def move_next(self, next_ch):
        curr_node = self.__curr_trie_node
        next_node = curr_node.get_next_ch(next_ch)
        if next_node is not None:
            self.__curr_trie_node = next_node
        else:
            next_node = TrieNode(next_ch, curr_node.get_depth()+1)
            next_node.find_max_suffix_equal_to_prefix(curr_node)
            self.__curr_trie_node = next_node.max_suffix_equal_to_prefix
        return [self.__curr_trie_node.get_depth(), self.__curr_trie_node.max_suffix_equal_to_search_str.get_depth(),
                self.__curr_trie_node.max_suffix_equal_to_search_str.get_replace_str()]

    def reset(self):
        self.__curr_trie_node = self.__head


if __name__ == '__main__':
    import io
    _search_replace_map = {'aaa': 'def', 'aba': ' ', 'ba': 'wsc'}
    trie = Trie(_search_replace_map)
    trie.print_trie()

    in_str = str('abdcbaababaaaba')
    trie.reset()
    for ch in in_str:
        print(trie.move_next(ch))

    # simple search and replace
    txt_str = str('abdcbaaababaaba')
    res_str = io.StringIO()
    trie.reset()
    b_indx = 0
    e_indx = 0
    while e_indx < len(txt_str):
        suffix_matching_len, suffix_search_str_matching_len, replace_str = trie.move_next(txt_str[e_indx])
        if suffix_search_str_matching_len:
            new_b_indx = e_indx - suffix_search_str_matching_len + 1
            if new_b_indx > b_indx:
                res_str.write(txt_str[b_indx:new_b_indx])
            res_str.write(replace_str)
            trie.reset()
            b_indx += suffix_matching_len

        elif e_indx - b_indx + 1 > suffix_matching_len:
            new_b_indx = e_indx - suffix_matching_len + 1
            res_str.write(txt_str[b_indx:new_b_indx])
            b_indx = new_b_indx
        e_indx += 1
    print(res_str.getvalue())



