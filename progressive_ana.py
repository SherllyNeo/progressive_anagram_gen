import math
from itertools import chain
import random

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.split_on = None
def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(f"{' ' * 10 * level}        {level}----> list: {node.data}, letter_to_ask: {node.split_on}")
        printTree(node.right, level + 1)


"""
Choose most common letter
Check letter is not common to all, if so try the next most common letter and so on. If it uses all letters then it will randomly choose one to filter by.
split by the most common letter
repeat on child nodes until length of data is 1




         "J",JacobX, BriX, JessyX
        /             \
"a", JacobX,JessyX     "BriX", None
                        /        \
     /         \       None      None
"JacobX"    "JessyX"
 /   \        /    \
None None    None  None

"""


class progressive_anagram_generator:
    def __init__(self,choices: list):
        """ init depth, max depth and the tree """
        self.depth_count = 0
        self.max_depth = 10000
        self.choices = sorted([choice.upper() for choice in choices])
        self.tree = Tree()
        self.tree.data = self.choices

    def frequency_dict_generator(self,list_: list) -> dict:
        """ It will return a dict of frequencies and preprocess """
        list_ = sorted([list(set(choice)) for choice in list_])

        frequency_dict = dict()
        for word in list_:
            for letter in word:
                if letter in frequency_dict:
                    frequency_dict[letter] += 1
                else:
                    frequency_dict[letter] = 1
        return frequency_dict
    def split_on_most_frequent_letter(self,frequency_dict: dict,list_: list):

        """ this function will use the frequency dict to find the most frequent letter and split a list by it. It will throw an error if all letters are equally frequent, it will choose the second most frequent letter if a split make a list of length None """
        inverted_dict = {u:v for v,u in frequency_dict.items()}
        max_key = max(inverted_dict.keys())
        most_frequent_letter = inverted_dict[max_key]
        left_list = [choice for choice in list_ if most_frequent_letter not in choice]
        right_list = [choice for choice in list_ if most_frequent_letter in choice]
        while len(left_list) == 0:
            inverted_dict_keys = list(inverted_dict.keys())
            inverted_dict_keys.remove(frequency_dict[most_frequent_letter])
            most_frequent_letter = inverted_dict[max(inverted_dict_keys)]
            left_list = [choice for choice in list_ if most_frequent_letter not in choice]
            right_list = [choice for choice in list_ if most_frequent_letter in choice]

        return left_list,right_list,most_frequent_letter



    def make_tree(self,tree):
        self.depth_count += 1
        if self.depth_count>self.max_depth:
            return
        if len(tree.data) == 1:
            return
        frequency_dict = self.frequency_dict_generator(tree.data)
        left_list,right_list,most_frequent_letter = self.split_on_most_frequent_letter(frequency_dict,tree.data)
        tree.right = Tree()
        tree.left = Tree()
        tree.split_on = most_frequent_letter
        tree.right.data = right_list
        tree.left.data = left_list
        self.make_tree(tree.right)
        self.make_tree(tree.left)


    def generate_progressive_anagram(self):
        progressive_anagram_tree = self.make_tree(self.tree)
        return self.tree


def entrypoint():
    choices = ["JessyX","KermitX","JacobX","XXBrian"]
    an_gen = progressive_anagram_generator(choices)
    tree  = an_gen.generate_progressive_anagram()
    print(f"making a progressive anagram for {choices}")
    printTree(tree)

entrypoint()
