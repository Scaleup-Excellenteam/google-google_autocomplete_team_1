from dataclasses import dataclass


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


class TrieTree:
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, line: str, filename: str) -> None:
        node = self.root
        # split the sentence to words and iterate over the words and insert to the tree as chain
        for word in line.split():
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

    def search(self, sentence: str) -> list[AutoCompleteData]:
        # first check if the sentence is in the tree and match any of the sentences in the tree
        # if was found match add to the result list
        # check if the array has 5 elements if not continue to search
        # searching for
        pass
