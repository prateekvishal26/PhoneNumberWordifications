from _collections import defaultdict


class TrieNode(object):
    """
    Initialize a Trie Node which has children and a bool indicating end of word.
    """

    def __init__(self):
        self.children = defaultdict()
        self.endOfWord = False


class Trie(object):

    def __init__(self):
        """
        Initialize Trie data structure
        """
        self.root = TrieNode()

    def insert(self, word):
        """
        Insert a word into the Trie. Repeatedly inserting all words produces the Trie data structure
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.endOfWord = True

    def search(self, word):
        """
        Returns True if the word is in the Trie else returns False.
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        if node.endOfWord:
            return True
        else:
            return False

    def starts_with(self, prefix):
        """
        Returns True if the prefix is in the Trie else returns False.
        """
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


class Dataset(object):
    """
    Generates the Dataset using the list of words from a text file
    """

    def __init__(self):
        self.wordsList = list()
        self.wordsDataset = Trie()
        self._read_file_data()
        self._generate_dataset()

    def _read_file_data(self):
        words_file = open("words.txt", "r")
        lines = words_file.readlines()
        for line in lines:
            data = line.split('\n')[0]
            if 1 < len(data) < 12:
                self.wordsList.append(data.upper())

    def _generate_dataset(self):
        for word in self.wordsList:
            self.wordsDataset.insert(word)


