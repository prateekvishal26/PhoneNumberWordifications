# Phone Number Wordifications
This repository represents a script which implements the functions words_to_num, num_to_words and all_wordifications

## Setup Instructions
1. Python 3.7 used for running and testing the script.
2. Modules such as itertools, collections and argparse were used from the Python Standard library.
3. Words dataset used from [https://raw.githubusercontent.com/dwyl/english-words/master/words.txt] to generate a dictionary of English words.

## Contents
1. [Problem Description](#1-problem-description)
2. [Implementation](#2-implementation)
3. [Running the Script](#3-running-the-script)

### 1. Problem Description 
The requirement is to implement three functions namely, words_to_num, num_to_words and all_wordifications. The function words_to_num returns a number that can be typed on a US keypad. The function num_to_word represents a wordified number and function all_wordifications represents all possible wordifications of the input number. It is assumed that all the words are from the words dataset which is a list of English words. These English words are stored in the form of a Trie data structure for efficient searching. The words used are of length between 2 and 10.

### 2. Implementation
1. __words_to_num__

Given an input of the wordified number, eg: "1800-PAINTER", the output is "1-800-724-6837". A dictionary of letters with their corresponding digits in the number keypad is used to return the number from the word. The number is checked for validity and hyphenated to the form X-XXX-XXX-XXXX and returned.

2. __num_to_words__

The input in this case is a number to be wordified number, eg: "1-800-724-6837", gives the output as "1800-PAINTER". The input is checked if it represents a valid US phone number. It then returns the wordified number containing the longest word. Here, it is assumed that the output contains only a single word from the dictionary. 

3. __all_wordifications__ 

For a given number, all wordifications are to be returned. First, it is checked if it represents a valid US phone number. Then all possible combinations of the number are obtained. Possible combinations of "1-800-724-6843" could be "1800-7246843" and "1-800-7246843". It is assumed that the two combinations represented earlier represent different combinations. Also, it is assumed that the combinations are such that maximum hyphens in a string are 3. So, a maximum of 4 words/numbers substrings could be obtained. Each substring is wordified and all combinations are returned. The wordification of a number are also stored in a dictionary. If a dictionary with all possible combinations of numbers is created then this function could be executed in a more time efficient way while compromising space efficiency.

### 3. Running the Script

Python script generate_dataset.py is used to generate the dataset which is a Trie data structure representing the dictionary of English words. The list of English words is used from words.txt. The script main.py contains the functions words_to_num, num_to_words and all_wordifications. The script can be run following the example given below. It is assumed that the script will be run to implement all three functions and therefore all three arguments --word_to_num, --num_to_word and --all_word should be populated with its inputs. Also, it is assumed that the function will be run for one input value at a time. 

```python main.py --word_to_num "1-800-PAINTER" --num_to_word "1-800-764-2643" --all_word "1-800-234-4376"```

	
