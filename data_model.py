from dataclasses import dataclass
from typing import Tuple, List, Any
import Levenshtein

MAX_RESULTS = 5

SUFFIX_DICT = {}
PREFIX_DICT = {}

SUB_SENTENCES_DICT = {}


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __str__(self):
        return f"{self.completed_sentence} ({self.source_text} {self.offset})"


class TrieNode:
    def __init__(self, word: str, depth_from_root: int = 0):
        self.children = {}
        self.is_end = False
        self.word = word
        self.filename = ""
        self.count = 0
        self.parent = None
        self.min_depth_to_leaf = 0  # for optimization of the dfs traversal
        self.start_from = {}  # to store a pointers to the root of the subtree that current node is contained in

    def update_end_of_line_chain(self, file_name: str) -> None:
        self.filename = file_name  # update the file name
        self.count += 1  # occurrences of the same sentence
        self.is_end = True  # end of line


def store_sub_sentences_in_dict(words, word_nodes):
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            sub_sentence = " ".join(words[i:j])
            SUB_SENTENCES_DICT.setdefault(sub_sentence, set()).add((word_nodes[words[i]], word_nodes[words[j - 1]]))
    # print(SUB_SENTENCES_DICT)


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
        word_nodes = {}  # for sub sentences
        if not words:
            return
        parent = None
        # self.starts_and_ends_with.setdefault(words[0], set())
        for i, word in enumerate(words, start=1):

            node = node.children.setdefault(word, TrieNode(word, i))
            word_nodes[word] = node
            # store the pointer to the node in the dictionary as set
            self.pointer_dict_to_words.setdefault(word, set()).add(node)
            if not node.parent:
                node.parent = parent
            parent = node
            # if not word == words[0]:
            #     self.starts_and_ends_with[words[0]].add(node)
            #
        node.update_end_of_line_chain(filename)
        store_sub_sentences_in_dict(words, word_nodes)

    @staticmethod
    def check_if_prefix_exists(self, node: TrieNode, prefix_words: list[str]) -> tuple[bool, str]:
        last_word_iterated = ""
        for i, word in enumerate(prefix_words):
            word = word.lower()

    def get_node_by_prefix(node: TrieNode, prefix: str) -> tuple[TrieNode, bool]:
        """
        this function iterate on chain of words based on the prefix and return the last node in the chain
        :param node: the root node
        :param prefix: the prefix to search
        :return: tuple of the last node in the chain and boolean if the prefix is in the tree
        """
        # is_exists = True
        # for word in prefix.split():
        #     if word in node.children:
        #         word = word.lower()
        #         last_word_iterated = word
        #         if node.children[word].min_depth_to_leaf < i:
        #             return False, last_word_iterated
        #         node = node.children[word]
        #     else:
        #         return False, last_word_iterated
        # return True, last_word_iterated
        # else:  # if the word is not in the tree
        #     is_exists = False

    # return node, is_exists

    def get_complete_sentences(self, node: TrieNode, last_node: TrieNode, sentence: str, output: list[AutoCompleteData],
                               is_single_word: bool = False) -> None:
        start_node = node
        # get the root of the subtree
        prefixes = []
        while node.parent:
            node = node.parent
            if node:
                prefixes.append(node.word)
        if prefixes:
            sentence = ' '.join(prefixes[::-1]) + ' ' + sentence
        # print(last_node.word, last_node.children)
        # print(last_node.word, last_node.children)
        # run dfs to get all possible sentences as suffix
        if last_node.is_end:
            output.append(AutoCompleteData(sentence, last_node.filename, last_node.count, 0))
        # [self.dfs(child, sentence, output) for child in last_node.children.values()]
        for child in last_node.children.values():
            print(child.word, child.children)
            if len(output) < MAX_RESULTS:
                self.dfs(child, sentence, output)
            else:
                break

    def search_and_get_k_suggestions(self, sentence: str, last_word: str, k=MAX_RESULTS) -> list[AutoCompleteData]:
        result_suggestions: list[AutoCompleteData] = []
        result = SUB_SENTENCES_DICT.get(sentence, set())
        is_single_word = len(sentence.split()) == 1
        if result:
            for first_node, last_node in result:
                self.get_complete_sentences(first_node, last_node, sentence, result_suggestions, is_single_word)
        return result_suggestions
        # # first check if the sentence is in the tree as prefix
        # prefix_words = sentence.split()
        # prefix_words = [word.lower() for word in sentence.split()]
        # node = self.root
        # last_word_iterated, is_prefix_in_tree = self.check_if_prefix_exists(node, prefix_words)
        #
        # if is_prefix_in_tree and not last_word_iterated.is_end:
        #     # make dfs iteration from the last word iterated
        #     self.dfs(last_word_iterated, sentence, result_suggestions, k)

        # starts_and_ends_with = self.starts_and_ends_with.get(prefix_words[0], set())
        # ends_with = self.starts_and_ends_with.get(last_word, set())
        # for v in starts_and_ends_with:
        #     if v in ends_with and v.depth_from_root == len(prefix_words):
        #         print(v.word, v.filename,v.depth_from_root)

        # node = get_last_node_by_prefix(node, prefix_words)
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
        # searching for additional methods to complete the sentence (add, remove, replace)
        # searching for additional methods to complete the sentence (add, remove, replace) using levenshtein distance

    @staticmethod
    def dfs(current_node: TrieNode, prefix: str, output: list[AutoCompleteData], k: int = MAX_RESULTS):
        if current_node.is_end:
            output.append(AutoCompleteData(prefix, current_node.filename, current_node.count, 0))
        for child in current_node.children.values():
            if len(output) < k:
                TrieTree.dfs(child, f"{prefix} {child.word}", output)
            else:
                break

    def add_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass
