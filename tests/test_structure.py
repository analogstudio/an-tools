import unittest
import an_tools.structure

class TestStructure(unittest.TestCase):

    def test_get_3dasset_dirname(self):       
        # create structure class
        structure = an_tools.structure.Structure()

        # assert the root is what is expected
        self.assertIsNotNone(structure.get_3dasset_dirname())

    def test_deprecated(self):       
        # create structure class
        structure = an_tools.structure.Structure()

        print('{n} - structure.get_dailies_url(): {v}'.format(n=__name__, v=structure.get_dailies_url()))
        print('{n} - structure.get_published_root(): {v}'.format(n=__name__, v=structure.get_published_root()))


if __name__ == '__main__':
    unittest.main()