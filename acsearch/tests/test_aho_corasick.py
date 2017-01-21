from nose.tools import (assert_equal,
                        assert_false,
                        assert_is,
                        assert_is_none,
                        assert_true)

from acsearch.aho_corasick import ACDictionary, ACRootNode


class TestACNode:
    def setup(self):
        self.root = ACRootNode()
        self.node_a = self.root.add_child('a', is_word=True)
        self.node_ab = self.node_a.add_child('b', is_word=True)
        self.node_b = self.root.add_child('b')
        self.node_ba = self.node_b.add_child('a')
        self.node_bab = self.node_ba.add_child('b', is_word=True)
        self.node_bc = self.node_b.add_child('c')
        self.node_bca = self.node_bc.add_child('a', is_word=True)
        self.node_c = self.root.add_child('c', is_word=True)
        self.node_ca = self.node_c.add_child('a')
        self.node_caa = self.node_ca.add_child('a', is_word=True)

    @staticmethod
    def _assert_node_ok(node, char, parent, is_word):
        (assert_true if char else assert_false)(node)
        assert_equal(node.char, char)
        assert_is(node.parent, parent)
        (assert_true if is_word else assert_false)(node.is_word)

    def test_init(self):
        self._assert_node_ok(self.root, None, self.root, False)
        self._assert_node_ok(self.node_a, 'a', self.root, True)
        self._assert_node_ok(self.node_ab, 'b', self.node_a, True)
        self._assert_node_ok(self.node_b, 'b', self.root, False)
        self._assert_node_ok(self.node_ba, 'a', self.node_b, False)
        self._assert_node_ok(self.node_bab, 'b', self.node_ba, True)
        self._assert_node_ok(self.node_bc, 'c', self.node_b, False)
        self._assert_node_ok(self.node_bca, 'a', self.node_bc, True)
        self._assert_node_ok(self.node_c, 'c', self.root, True)
        self._assert_node_ok(self.node_ca, 'a', self.node_c, False)
        self._assert_node_ok(self.node_caa, 'a', self.node_ca, True)

    def test_add_child(self):
        node_aa = self.node_a.add_child('a')
        self._assert_node_ok(node_aa, 'a', self.node_a, False)

        node_aa_ = self.node_a.add_child('a', is_word=True)
        assert_is(node_aa, node_aa_)
        assert_true(node_aa.is_word)

    @staticmethod
    def _assert_node_str_ok(node, str_):
        assert_equal(node.get_chars(), list(str_))
        assert_equal(str(node), str_)
        assert_equal(len(node), len(str_))

    def test_str(self):
        self._assert_node_str_ok(self.root, '')
        self._assert_node_str_ok(self.node_a, 'a')
        self._assert_node_str_ok(self.node_ab, 'ab')
        self._assert_node_str_ok(self.node_b, 'b')
        self._assert_node_str_ok(self.node_ba, 'ba')
        self._assert_node_str_ok(self.node_bab, 'bab')
        self._assert_node_str_ok(self.node_bc, 'bc')
        self._assert_node_str_ok(self.node_bca, 'bca')
        self._assert_node_str_ok(self.node_c, 'c')
        self._assert_node_str_ok(self.node_ca, 'ca')
        self._assert_node_str_ok(self.node_caa, 'caa')

    def test_suffix(self):
        assert_is(self.root.suffix, self.root)
        assert_is(self.node_a.suffix, self.root)
        assert_is(self.node_ab.suffix, self.node_b)
        assert_is(self.node_b.suffix, self.root)
        assert_is(self.node_ba.suffix, self.node_a)
        assert_is(self.node_bab.suffix, self.node_ab)
        assert_is(self.node_bc.suffix, self.node_c)
        assert_is(self.node_bca.suffix, self.node_ca)
        assert_is(self.node_c.suffix, self.root)
        assert_is(self.node_ca.suffix, self.node_a)
        assert_is(self.node_caa.suffix, self.node_a)

    def test_dict_suffix(self):
        assert_is_none(self.root.dict_suffix)
        assert_is_none(self.node_a.dict_suffix)
        assert_is_none(self.node_ab.dict_suffix)
        assert_is_none(self.node_ab.dict_suffix)
        assert_is(self.node_ba.dict_suffix, self.node_a)
        assert_is(self.node_bab.dict_suffix, self.node_ab)
        assert_is(self.node_bc.dict_suffix, self.node_c)
        assert_is(self.node_bca.dict_suffix, self.node_a)
        assert_is_none(self.node_c.dict_suffix)
        assert_is(self.node_ca.dict_suffix, self.node_a)
        assert_is(self.node_caa.dict_suffix, self.node_a)

    def test_get_next(self):
        assert_is(self.root.get_next('a'), self.node_a)
        assert_is(self.root.get_next('b'), self.node_b)
        assert_is(self.root.get_next('c'), self.node_c)
        assert_is(self.root.get_next('x'), self.root)

        assert_is(self.node_a.get_next('a'), self.node_a)
        assert_is(self.node_a.get_next('b'), self.node_ab)
        assert_is(self.node_a.get_next('c'), self.node_c)
        assert_is(self.node_a.get_next('x'), self.root)

        assert_is(self.node_ab.get_next('a'), self.node_ba)
        assert_is(self.node_ab.get_next('b'), self.node_b)
        assert_is(self.node_ab.get_next('c'), self.node_bc)
        assert_is(self.node_ab.get_next('x'), self.root)

        assert_is(self.node_b.get_next('a'), self.node_ba)
        assert_is(self.node_b.get_next('b'), self.node_b)
        assert_is(self.node_b.get_next('c'), self.node_bc)
        assert_is(self.node_b.get_next('x'), self.root)

        assert_is(self.node_ba.get_next('a'), self.node_a)
        assert_is(self.node_ba.get_next('b'), self.node_bab)
        assert_is(self.node_ba.get_next('c'), self.node_c)
        assert_is(self.node_ba.get_next('x'), self.root)

        assert_is(self.node_bab.get_next('a'), self.node_ba)
        assert_is(self.node_bab.get_next('b'), self.node_b)
        assert_is(self.node_bab.get_next('c'), self.node_bc)
        assert_is(self.node_bab.get_next('x'), self.root)

        assert_is(self.node_bc.get_next('a'), self.node_bca)
        assert_is(self.node_bc.get_next('b'), self.node_b)
        assert_is(self.node_bc.get_next('c'), self.node_c)
        assert_is(self.node_bc.get_next('x'), self.root)

        assert_is(self.node_bca.get_next('a'), self.node_caa)
        assert_is(self.node_bca.get_next('b'), self.node_ab)
        assert_is(self.node_bca.get_next('c'), self.node_c)
        assert_is(self.node_bca.get_next('x'), self.root)

        assert_is(self.node_c.get_next('a'), self.node_ca)
        assert_is(self.node_c.get_next('b'), self.node_b)
        assert_is(self.node_c.get_next('c'), self.node_c)
        assert_is(self.node_c.get_next('x'), self.root)

        assert_is(self.node_ca.get_next('a'), self.node_caa)
        assert_is(self.node_ca.get_next('b'), self.node_ab)
        assert_is(self.node_ca.get_next('c'), self.node_c)
        assert_is(self.node_ca.get_next('x'), self.root)

        assert_is(self.node_caa.get_next('a'), self.node_a)
        assert_is(self.node_caa.get_next('b'), self.node_ab)
        assert_is(self.node_caa.get_next('c'), self.node_c)
        assert_is(self.node_caa.get_next('x'), self.root)

    def test_get_words(self):
        assert_equal(list(self.root.get_words()), [])
        assert_equal(list(self.node_a.get_words()), [self.node_a])
        assert_equal(list(self.node_ab.get_words()), [self.node_ab])
        assert_equal(list(self.node_b.get_words()), [])
        assert_equal(list(self.node_ba.get_words()), [self.node_a])
        assert_equal(list(self.node_bab.get_words()),
                     [self.node_bab, self.node_ab])
        assert_equal(list(self.node_bc.get_words()), [self.node_c])
        assert_equal(list(self.node_bca.get_words()),
                     [self.node_bca, self.node_a])
        assert_equal(list(self.node_c.get_words()), [self.node_c])
        assert_equal(list(self.node_ca.get_words()), [self.node_a])
        assert_equal(list(self.node_caa.get_words()),
                     [self.node_caa, self.node_a])


class TestACDictionary:
    def setup(self):
        self.words = {'a', 'ab', 'bab', 'c', 'bca', 'caa'}
        self.acd = ACDictionary(self.words)

    def test_init(self):
        nodes_df = list(self.acd._nodes(sort=True))
        assert_equal(
            [str(node) for node in nodes_df],
            ['', 'a', 'ab', 'b', 'ba', 'bab', 'bc', 'bca', 'c', 'ca', 'caa']
        )

        nodes_bf = list(self.acd._nodes(sort=True, bf=True))
        assert_equal(
            [str(node) for node in nodes_bf],
            ['', 'a', 'b', 'c', 'ab', 'ba', 'bc', 'ca', 'bab', 'bca', 'caa']
        )

    def test_len(self):
        assert_equal(len(self.acd), len(self.words))

    def test_iter(self):
        assert_equal(list(self.acd), sorted(self.words))

    def test_findall(self):
        assert_equal(self.acd.findall('abccabx'),
                     ['a', 'ab', 'c', 'c', 'a', 'ab'])

    def test_finditer(self):
        assert_equal([(m.start, m.end, str(m))
                      for m in list(self.acd.finditer('abccabx'))],
                     [(0, 1, 'a'),
                      (0, 2, 'ab'),
                      (2, 3, 'c'),
                      (3, 4, 'c'),
                      (4, 5, 'a'),
                      (4, 6, 'ab')])
