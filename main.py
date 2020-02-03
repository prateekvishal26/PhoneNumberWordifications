import itertools
from collections import defaultdict
from generate_dataset import Dataset
import argparse



class Wordify(object):
    """
    Implements the functions words_to_number(), all_wordifications() and number_to_words()
    """

    def __init__(self):
        self.numpadHash = dict()
        self.letterHash = dict()
        self._hash_generate()
        self.hyphen = '-'
        data = Dataset()
        self.wordsDictionary = data.wordsDataset
        self.allWords = defaultdict()
        self.allWordifications = defaultdict()
        self.allCombinations = list()
        self.maximumHyph = 3

    def _hash_generate(self):
        """
        Generates dictionary of numpad mapping numbers to letters and another dictionary to map letters to numbers
        """
        self.numpadHash = {'2': ['A', 'B', 'C'], '3': ['D', 'E', 'F'], '4': ['G', 'H', 'I'],
                           '5': ['J', 'K', 'L'], '6': ['M', 'N', 'O'], '7': ['P', 'Q', 'R', 'S'],
                           '8': ['T', 'U', 'V'], '9': ['W', 'X', 'Y', 'Z']}
        for n in self.numpadHash:
            for letter in self.numpadHash[n]:
                self.letterHash[letter] = str(n)

    def _check_valid_number(self, number):
        """
        Returns True if number is a valid US phone number(11 digit long)
        """
        number = self._de_hyphenate_number(number)
        length = 0
        for ch in number:
            if ch != 0 <= int(ch) <= 9:
                length += 1
        if length == 11:
            return True
        else:
            return False

    def _hyphenate_number(self, number):
        """
        Returns the number in the form X-XXX-XXX-XXXX
        """
        number = self._de_hyphenate_number(number)
        number = number[0] + self.hyphen + number[1:]
        number = number[0:5] + self.hyphen + number[5:]
        number = number[0:9] + self.hyphen + number[9:]
        return number

    def _de_hyphenate_number(self, number):
        """
        Returns the number as a string without hyphens
        """
        number = number.replace(self.hyphen, "")
        return number

    def _get_string(self, l):
        """
        Returns the string from the given list
        """
        str = ""
        for i in l:
            if i == '\0':
                return str
            str += i

    def _get_all_combinations_recurse(self, number, comb, i, j, n):
        """
        Recursively runs to append to the list of all possible combinations of the given number
        """
        if i == n:
            comb[j] = '\0'
            comb_str = self._get_string(comb)
            self.allCombinations.append(comb_str)
            return
        comb[j] = number[i]
        self._get_all_combinations_recurse(number, comb, i + 1, j + 1, n)
        comb[j] = '-'
        comb[j + 1] = number[i]
        self._get_all_combinations_recurse(number, comb, i + 1, j + 2, n)

    def _get_all_combinations(self, number):
        """
        Gets all possible combinations of the given number
        """
        n = len(number)
        temp = [0] * (2 * n)
        temp[0] = number[0]
        self.allCombinations = list()
        self._get_all_combinations_recurse(number, temp, 1, 1, n)
        return

    def _get_filtered_combinations(self):
        """
        Gets all possible combinations of the given number where maximum hyphens are 3
        """
        filtered_combinations = list()
        for comb in self.allCombinations:
            if comb.count('-') <= self.maximumHyph:
                filtered_combinations.append(comb)
        return filtered_combinations

    def _wordify_number(self, number):
        """
        Return the wordified number for the given combination
        """
        substr_list = number.split(self.hyphen)
        wordified_list = list()
        for substr in substr_list:
            wordified_list.append(self._wordify(substr))
        all_combinations = list(itertools.product(*wordified_list))
        all_wordified_combinations = list()
        for wordified_combinations in all_combinations:
            all_wordified_combinations.append(self.hyphen.join([str(elem) for elem in wordified_combinations]))
        return all_wordified_combinations

    def _wordify(self, number):
        """
        Return the wordified number given a substring. Eg: "7246837" returns "PAINTER"
        """
        if number not in self.allWords:
            self.allWords[number] = list()
            words = list()
            for ind, n in enumerate(number):
                if n in self.numpadHash:
                    new_words = list()
                    if len(words) == 0:
                        words = self.numpadHash[n]
                        continue
                    for wrd in words:
                        for ch in self.numpadHash[n]:
                            wd = wrd + ch
                            if self.wordsDictionary.starts_with(wd):
                                new_words.append(wd)
                    words = new_words
                else:
                    self.allWords[number].append(number)
                    words = list()
                    break
            if len(words) == 0 and len(self.allWords[number]) == 0:
                self.allWords[number].append(number)

            for w in words:
                if self.wordsDictionary.search(w):
                    self.allWords[number].append(w)
        return tuple(self.allWords[number])

    def words_to_number(self, word):
        """
        Returns the number given a wordified number as input
        """
        number = ""
        for ch in word:
            if ch in self.letterHash:
                number += self.letterHash[ch]
            else:
                number += ch
        if self._check_valid_number(number):
            return self._hyphenate_number(number)
        else:
            return "Invalid Number"

    def number_to_words(self, number):
        """
        Returns the wordified number with longest word that can be obtained
        """
        list_of_words = dict()
        words = list()
        if self._check_valid_number(number):
            number = self._de_hyphenate_number(number)
        else:
            return "Invalid Number"
        for ind, n in enumerate(number):
            if n in self.numpadHash:
                new_words = list()
                if len(words) == 0:
                    words = self.numpadHash[n]
                    continue
                for wrd in words:
                    for ch in self.numpadHash[n]:
                        wd = wrd + ch
                        if self.wordsDictionary.search(wd):
                            wordified_num = number[0:ind - len(wd) + 1] + self.hyphen + wd + self.hyphen + number[
                                                                                                           ind + 1:]
                            if wordified_num[-1] == self.hyphen:
                                wordified_num = wordified_num[0:-1]
                            if len(wd) not in list_of_words:
                                list_of_words[len(wd)] = wordified_num
                            new_words.append(wd)
                        elif self.wordsDictionary.starts_with(wd):
                            new_words.append(wd)
                    words = new_words
            else:
                words = list()
        return list_of_words[max(list_of_words.keys())]

    def all_wordifications(self, number):
        """
        Returns all possible wordifications of given number
        """
        if self._check_valid_number(number):
            number = self._de_hyphenate_number(number)
        else:
            return "Invalid Number"
        if number not in self.allWordifications:
            self.allWordifications[number] = list()
        self._get_all_combinations(number)
        filtered_combinations = self._get_filtered_combinations()
        for combination in filtered_combinations:
            wordified_number = self._wordify_number(combination)
            for w_n in wordified_number:
                if self._de_hyphenate_number(w_n) != self._de_hyphenate_number(combination):
                    self.allWordifications[number].append(w_n)

        return self.allWordifications[number]


if __name__ == '__main__':
    w = Wordify()
    try:
        arg = argparse.ArgumentParser()
        arg.add_argument("--word_to_num", "--word_to_num", required=True,
                        help="Input word to word_to_num")
        arg.add_argument("--num_to_word", "--num_to_word", required=True,
                         help="Input word to word_to_num")
        arg.add_argument("--all_word", "--all_word", required=True,
                         help="Input word to word_to_num")
        args = vars(arg.parse_args())

        print("Printing words to number for input {0}:".format(args['word_to_num']))
        print(w.words_to_number(str(args['word_to_num'])))
        print("Printing number to words for input {0}:".format(args['num_to_word']))
        print(w.number_to_words(str(args['num_to_word'])))
        print("Printing all wordifications for input {0}:".format(args['all_word']))
        print(w.all_wordifications(str(args['all_word'])))
    except Exception as e:
        print("Exception occurred: {0}".format(str(e)))
        print("Printing words to number for input 1-800-PAINTER:")
        print(w.words_to_number('1-800-PAINTER'))
        print("Printing number to words for input 1-800-724-6837:")
        print(w.number_to_words("1-800-724-6837"))
        print("Printing all wordifications for input 1-800-724-6837:")
        print(w.all_wordifications("1-800-724-6837"))

