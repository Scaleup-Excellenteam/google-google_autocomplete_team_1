import os
from typing import List
from data_model import AutoCompleteData, TrieTree

BASE_DIR = 'Archive'
RESET_STATE_SYMBOL = '#'
LOADING_AND_PREPARING_SYSTEM = 'Loading and preparing the system...'
SYSTEM_READY = 'The system is ready. Enter your text:'
K = 5

TOP_K_RESULTS = f'Here are the top {K} results:'


def get_best_k_ֵcompletions(prefix: str) -> List[AutoCompleteData]:
    pass


# init the data model(loading the data from the files and store in the data model-trie tree)
def get_files_from_folder(folder_path: str, trie_tree: TrieTree) -> None:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        trie_tree.insert(line, file_path)


def initialize_data_model(root_folder_path: str, trie_tree: TrieTree) -> None:
    get_files_from_folder(BASE_DIR, trie_tree)


def main():
    # parser = argparse.ArgumentParser(description='AutoCompleteSystem')
    # parser.add_argument('root_folder_path', type=str, help='The root directory of the project')
    # args = parser.parse_args()
    # root_folder_path = args.root_folder_path or BASE_DIR
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
    while True:
        user_input = input()
        if user_input.endswith(RESET_STATE_SYMBOL):
            print(SYSTEM_READY)
            continue
        # autocomplete_results = get_best_k_ֵcompletions(prefix)
        print(TOP_K_RESULTS)
        # print(autocomplete_results)
        print('test')


if __name__ == "__main__":
    main()
