from dataclasses import dataclass
from typing import Tuple, List, Any
import Levenshtein

MAX_RESULTS = 5

SUFFIX_DICT = {}
PREFIX_DICT = {}


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offֵset: int
    score: int


class TrieNode:
    def __init__(self, word: str, depth_from_root: int = 0):
        self.children = {}
        self.is_end = False
        self.word = word
        self.filename = ""
        self.count = 0
        self.start_from = {}  # to store a pointers to the root of the subtree that current node is contained in

    def update_end_of_line_chain(self, file_name: str) -> None:
        self.filename = file_name  # update the file name
        self.count += 1  # occurrences of the same sentence
        self.is_end = True  # end of line


class TrieTree:
    def __init__(self):
        self.root = TrieNode("")
        # dictionary that store the pointer for places of the words in tree
        self.pointer_dict_to_words = {}
        # self.starts_and_ends_with = {}

    def insert(self, line: str, filename: str) -> None:
        node = self.root
        # split the sentence to words and iterate over the words and insert to the tree as chain
        words = list(map(lambda word: word.lower(), line.split()))
        if not words:
            return
        self.starts_and_ends_with.setdefault(words[0], set())
        for i, word in enumerate(words, start=1):
            node = node.children.setdefault(word, TrieNode(word, i))
            # store the pointer to the node in the dictionary as set
            self.pointer_dict_to_words.setdefault(word, set()).add(node)
            if not word == words[0]:
                self.starts_and_ends_with[words[0]].add(node)

            # print(self.pointer_dict_to_words)
            # print(self.starts_and_ends_with)
            # Prefix and suffix dict for levenshtein distance
            for i in range(len(word)):
                SUFFIX_DICT.setdefault(word[i:], set()).add(node)
                PREFIX_DICT.setdefault(word[:i + 1], set()).add(node)

    def get_all_sentences(self, node: TrieNode, prefix: str, output: list[AutoCompleteData], k: int = MAX_RESULTS):
        if len(output) >= k:
            return
        if node.is_end:
            output.append(AutoCompleteData(prefix, node.filename, 0, 0))
        for child in node.children.values():
            if len(output) < k:
                self.get_all_sentences(child, f"{prefix} {child.word}", output, k)
            else:
                break

    @staticmethod
    def get_node_by_prefix(node: TrieNode, prefix: str) -> tuple[TrieNode, bool]:
        """
        this function iterate on chain of words based on the prefix and return the last node in the chain
        :param node: the root node
        :param prefix: the prefix to search
        :return: tuple of the last node in the chain and boolean if the prefix is in the tree
        """
        is_exists = True
        for word in prefix.split():
            if word in node.children:
                node = node.children[word]
            else:  # if the word is not in the tree
                is_exists = False
        return node, is_exists

    def search_and_get_k_suggestions(self, sentence: str, last_word: str, k=MAX_RESULTS) -> list[AutoCompleteData]:
        result_suggestions: list[AutoCompleteData] = []
        # first check if the sentence is in the tree as prefix
        prefix_words = [word.lower() for word in sentence.split()]
        node = self.root
        # starts_and_ends_with = self.starts_and_ends_with.get(prefix_words[0], set())
        # ends_with = self.starts_and_ends_with.get(last_word, set())
        # for v in starts_and_ends_with:
        #     if v in ends_with and v.depth_from_root == len(prefix_words):
        #         print(v.word, v.filename,v.depth_from_root)

        node = get_last_node_by_prefix(node, prefix_words)
        # start_nodes = self.pointer_dict_to_words.get(last_word)
        # for start_node in start_nodes:

        # print(start_nodes)
        # if start_nodes:
        #     for start_node in start_nodes:
        #         ends_with = self.starts_and_ends_with.get(prefix_words[0])
        #         matching = list(filter(lambda node: node in ends_with and node.depth_from_root == len(prefix_words),
        #                                start_node.children.values()))

        # print(result_suggestions)
        # if was found match add to the result list
        # check if the array has 5 elements if not continue to search
        # searching for additional methods to complete the sentence (add, remove, replace) using levenshtein distance

    @staticmethod
    def dfs(current_node: TrieNode, prefix: str, output: list[AutoCompleteData], k: int = MAX_RESULTS):
        if current_node.is_end:
            output.append(AutoCompleteData(prefix, current_node.filename, 0, 0))
        for child in current_node.children.values():
            if len(output) < k:
                TrieTree.dfs(child, f"{prefix} {child.word}", output, k)
            else:
                break

    def add_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass

    def replace_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass

    def remove_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass

    def test(self, word):
        print("possible chains for word:", word)
        for i, chain in enumerate(self.pointer_dict_to_words[word]):
            print(i, chain.word)

    def get_sentence_by_node_pointer(self, node_pointer: TrieNode, offset: int) -> str:
        """
        get the sentence by the node pointer and offset
        :param node_pointer: the pointer to the node
        :param offset: the offset of the sentence in the file
        :return: the sentence
        """
