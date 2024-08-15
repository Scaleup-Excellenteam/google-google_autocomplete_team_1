import os
from typing import List
from data_model import TrieTree

RESET_STATE = 'Enter new sentence: '
BASE_DIR = 'Archive'
RESET_STATE_SYMBOL = '#'
LOADING_AND_PREPARING_SYSTEM = 'Loading and preparing the system...'
ENTER_SENTENCE = 'Enter your text: '
SYSTEM_READY = 'The system is ready. Enter your text:'
TOP_K_RESULTS = 'Here are the top 5 results:'


def initialize_data_model(root_folder_path: str, trie_tree: TrieTree) -> None:
    """
    This function is responsible for loading the data from the files and store in the data model-trie tree
    :param root_folder_path: main folder path
    :param trie_tree: the trie tree
    :return: None
    """
    # for root, dirs, files in os.walk(folder_path):
    #     for file in files:
    #         if file.endswith(".txt"):
    #             file_path = os.path.join(root, file)
    file_path = 'test.txt'
    with open(file_path, 'r') as f:
        for line in f:
            trie_tree.insert(line, file_path)
    # to_test = SUB_SENTENCES_DICT.get("am a developer", set())
    # if to_test:
    #     trie_tree.get_sentence_by_node(to_test.pop())


def main() -> None:
    # parser = argparse.ArgumentParser(description='AutoCompleteSystem')
    # parser.add_argument('root_folder_path', type=str, help='The root directory of the project')
    # args = parser.parse_args()
    root_folder_path = BASE_DIR
    if not os.path.exists(root_folder_path):
        print(f'The path {root_folder_path} does not exist')
        return

    trie_tree = TrieTree()
    print(LOADING_AND_PREPARING_SYSTEM)
    initialize_data_model(root_folder_path, trie_tree)
    # load_and_prepare_system()
    # start the cli
    print(SYSTEM_READY)
    user_input = ""
    while True:
        current_user_input = input(ENTER_SENTENCE + user_input)
        if current_user_input == RESET_STATE_SYMBOL:
            user_input = input(RESET_STATE)
        else:
            user_input += current_user_input
        # autocomplete_results = get_best_k_ֵcompletions(prefix)
        print(TOP_K_RESULTS)
        # print(autocomplete_results)
        last_word = user_input.split()[-1]
        result = trie_tree.search_and_get_k_suggestions(sentence=user_input, last_word=last_word)
        for i, res in enumerate(result):
            print(f'{i + 1}. {res}')


if __name__ == "__main__":
    main()
