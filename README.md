# google_autocomplete_team_1

## Overview

This project is a command line interface for autocomplete suggestions for user input(as a prefix).
the data is read from files a lines in a directory and stored in a trie data structure.

## Features

- Autocomplete suggestions based on user input
- Suggests the top K sentences that start with the given prefix
- suggestion with insertion/deletion or replacement of a character for mismatched prefix

## Algorithms & Structures

* Data Structures:
  using a trie to store the lines as a broken words
  first we will read from the files
  then we will store the lines in the trie
  iterate over the lines and store each word in the trie as chain of nodes
  if the line already exists in the trie so the counter will be increased by one and update the last word in the line

for example:
"this is a line" will be stored as:

```
this -> is -> a -> line
```

then adding "this is a line 2" will be stored as:
the prefix "this is a line" already exists then we will chain the word "2" to the last node in the line

```
this is a line -> 2
```

* Algorithms

    * search algorithm:
      - first ,check if the word is in the trie or not as a prefix
      if it is a prefix then we will iterate over the children of the last node in the prefix and get the top 5 words by
      traverse algorithm(dfs for iterate over its suggestions - all the lines that start with the prefix)
      if the top 5 words are less than 5 then we will get the rest of the words from the trie by traverse algorithm
      if was not a prefix so return empty list
      for reaching 5 words we will try to modify start from last char in the prefix and try to get the top 5 words from
      the trie
      - then we will try to modify the prefix by deleting/insert/replace the last char and try to get the top 5 words from the trie
      - some improvements: adding a variable that store the minimal num of the current node to skip unnecessary dfs iterations
* ## Detailed Code Flow

At first, I thought about using hash map or red black tree but then I found that trie is the best data structure for
this
problem

**Hint**: This section is just a placeholder example of fruit prices. Replace it with a clear and detailed flow of your
actual project's logic, algorithms, and processes.
