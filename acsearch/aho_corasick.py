"""
Implementation of the Aho-Corasick string search algorithm.

See https://en.wikipedia.org/wiki/Aho-Corasick_algorithm
"""

from collections import deque
from functools import wraps


def cached_property(method):
    """ Decorator to create a lazy property that is cached on first access """
    attr = '_'+method.__name__

    @property
    @wraps(method)
    def func(self):
        try:
            return getattr(self, attr)
        except AttributeError:
            value = method(self)
            setattr(self, attr, value)
            return value

    return func


class ACDictionary:
    """
    Dictionary of words that builds an Aho-Corasick tree to support efficient
    string search.
    """
    def __init__(self, words):
        """
        Initialize the dictionary with the given words. The dictionary does not
        support modification once initialized.
        """
        self._root = ACRootNode()
        self._len = sum(1 for word in words if self._add_word(word))

    def _add_word(self, word):
        node = self._root
        for char in word:
            node = node.add_child(char)
        if node:
            was_word = node.is_word
            node.is_word = True
            return not was_word
        else:
            raise ValueError("Empty word: {!r}".format(word))

    def findall(self, text):
        """
        Return a list of dictionary words contained in the given text. Each word
        will appear once per occurrence in the text.
        """
        return [str(wnode) for end, wnode in self._find(text)]

    def finditer(self, text):
        """
        Yield a sequence of ACMatch objects for each dictionary word contained
        in the given text.
        """
        for end, wnode in self._find(text):
            yield ACMatch(text, end-len(wnode), end)

    def _find(self, text):
        node = self._root
        for end, c in enumerate(text, 1):
            node = node.get_next(c)
            for wnode in node.get_words():
                yield (end, wnode)

    def _nodes(self, bf=False, sort=False):
        nodes = deque()
        nodes.append(self._root)
        while nodes:
            node = nodes.popleft() if bf else nodes.pop()
            yield node
            nodes.extend((v for k,v in sorted(node.children.items(),
                                              reverse=not bf))
                         if sort else node.children.values())

    def __iter__(self):
        """ Yield the words in the dictionary in sorted order """
        for node in self._nodes(sort=True):
            if node.is_word:
                yield str(node)

    def __len__(self):
        return self._len


class ACMatch:
    """ Object representing a matching substring of a given query """
    def __init__(self, string, start, end):
        self.string = string
        self.start = start
        self.end = end

    def __str__(self):
        return self.string[self.start:self.end]


class ACNode:
    """ Aho-Corasick tree node """
    def __init__(self, char, parent, is_word=False):
        self.char = char
        self.parent = parent
        self.is_word = is_word
        self.children = {}
        self.len = parent.len + 1

    def add_child(self, char, is_word=False):
        """
        Add a child node containing the given char with the given word status.

        If a child node already exists for the given char, its word status will
        be or-ed with the given word_status.

        Returns the child node.
        """
        child = self.children.get(char)

        if child:
            # Update word status of child
            child.is_word = child.is_word or is_word
        else:
            # Create new child
            child =  ACNode(char, self, is_word)
            self.children[char] = child

        return child

    # Note: should not be accessed until the tree is fully built.
    @cached_property
    def suffix(self):
        """
        Return the node corresponding to the longest dictionary prefix that is
        a proper suffix of the current node.
        """
        return (self.parent.suffix.get_next(self.char)
                if self.parent else self.parent)

    # Note: should not be accessed until the tree is fully built.
    @cached_property
    def dict_suffix(self):
        """
        Return the node corresponding to the longest dictionary word that is a
        proper suffix of the current node, or None if no such node exists.
        """
        if self.suffix.is_word:
            return self.suffix
        else:
            return self.suffix.dict_suffix

    def get_next(self, char):
        """
        Return the node corresponding to the longest dictionary prefix that is
        a suffix of the given char appended to the current node.
        """
        if char in self.children:
            return self.children[char]
        else:
            return self.suffix.get_next(char)

    def get_words(self):
        """
        Yield all nodes corresponding to dictionary words that are suffixes of
        the current node.
        """
        node = self
        while node:
            if node.is_word:
                yield node
            node = node.dict_suffix

    def get_chars(self):
        """
        Return a list of characters for the given node.
        """
        chars = self.parent.get_chars()
        chars.append(self.char)
        return chars

    def __str__(self):
        return ''.join(self.get_chars())

    def __len__(self):
        return self.len
        

class ACRootNode(ACNode):
    """ Aho-Corasick root node """
    def __init__(self):
        self.char = None
        self.parent = self
        self.is_word = False
        self.children = {}
        self.len = 0
        self._dict_suffix = None

    def get_next(self, char):
        if char in self.children:
            return self.children[char]
        else:
            return self

    def get_chars(self):
        return []
