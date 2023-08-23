from dataclasses import dataclass

MAX_RESULTS = 5


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offֵset: int
    score: int


class TrieNode:
    def __init__(self, sentence: str):
        self.children = {}
        self.is_end = False
        self.sentence = sentence
        self.filename = ""
        self.count = 0
        self.min_depth_to_leaf = 0  # for optimization of the dfs traversal


class TrieTree:
    def __init__(self):
        self.root = TrieNode("")

    # todo: update min_depth_to_leaf
    def insert(self, line: str, filename: str) -> None:
        node = self.root
        # split the sentence to words and iterate over the words and insert to the tree as chain
        for word in line.split():
            word = word.lower()
            if word in node.children:
                node.children[word] = TrieNode(word)
            else:
                new_node = TrieNode(word)
                node.children[word] = new_node
                node = new_node
        # if already exists in the tree so update the node
        node.is_end = True  # end of line
        node.count += 1  # same line already exists
        node.filename = filename

    @staticmethod
    def check_if_prefix_exists(self, node: TrieNode, prefix_words: list[str]) -> tuple[bool, str]:
        last_word_iterated = ""
        for i, word in enumerate(prefix_words):
            word = word.lower()
            if word in node.children:
                word = word.lower()
                last_word_iterated = word
                if node.children[word].min_depth_to_leaf < i:
                    return False, last_word_iterated
                node = node.children[word]
            else:
                return False, last_word_iterated
        return True, last_word_iterated

    def search_and_get_k_suggestions(self, sentence: str, k=MAX_RESULTS) -> list[AutoCompleteData]:
        result_suggestions = []
        # first check if the sentence is in the tree as prefix
        prefix_words = sentence.split()
        node = self.root
        last_word_iterated, is_prefix_in_tree = self.check_if_prefix_exists(node, prefix_words)


        if is_prefix_in_tree and not last_word_iterated.is_end:
            # make dfs iteration from the last word iterated
            self.dfs(last_word_iterated, sentence, result_suggestions, k)


        # if was found match add to the result list
        # check if the array has 5 elements if not continue to search
        # searching for additional methods to complete the sentence (add, remove, replace)

    @staticmethod
    def dfs(current_node: TrieNode, prefix: str, output: list[AutoCompleteData], k: int = MAX_RESULTS):
        pass

    def add_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass

    def replace_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass

    def remove_char(self, current_node: TrieNode, prefix: str, output: list[AutoCompleteData]):
        pass
