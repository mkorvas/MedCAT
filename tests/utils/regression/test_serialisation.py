
import unittest

from medcat.utils.regression.targeting import CUIWithChildFilter, FilterType, FilterStrategy, FilterOptions
from medcat.utils.regression.targeting import TypedFilter, TranslationLayer
from medcat.utils.regression.checking import RegressionChecker, RegressionCase


class TestSerialisation(unittest.TestCase):

    def test_TypedFilter_serialises(self, ft=FilterType.NAME, vals=['FNAME1', 'FNAME2']):
        tf = TypedFilter(type=ft, values=vals)
        self.assertIsInstance(tf.to_dict(), dict)

    def test_TypedFilter_deserialises(self, ft=FilterType.NAME, vals=['FNAME-1', 'FNAME=2']):
        tf = TypedFilter(type=ft, values=vals)
        tf2 = TypedFilter.from_dict(tf.to_dict())[0]
        self.assertIsInstance(tf2, TypedFilter)

    def test_TypedFilter_deserialises_to_one(self, ft=FilterType.NAME, vals=['FNAME-1', 'FNAME=2']):
        tf = TypedFilter(type=ft, values=vals)
        l = TypedFilter.from_dict(tf.to_dict())
        self.assertEqual(len(l), 1)

    def test_TypedFilter_deserialises_to_same(self, ft=FilterType.NAME, vals=['FNAME-1', 'FNAME=2']):
        tf = TypedFilter(type=ft, values=vals)
        tf2 = TypedFilter.from_dict(tf.to_dict())[0]
        self.assertEqual(tf, tf2)

    def test_CUIWithChildFilter_deserialises_to_same(self, cui='the-cui', depth=5):
        delegate = TypedFilter(type=FilterType.CUI_AND_CHILDREN, values=[cui])
        tf = CUIWithChildFilter(
            type=FilterType.CUI_AND_CHILDREN, depth=depth, delegate=delegate)
        tf2 = TypedFilter.from_dict(tf.to_dict())[0]
        print('TF dict', tf.to_dict())
        self.assertIsInstance(tf2, CUIWithChildFilter)
        print('tf1', tf)
        print('vs')
        print('tf2', tf2)
        self.assertEqual(tf, tf2)

    def test_multiple_TypedFilter_serialise(self, ft1=FilterType.NAME, ft2=FilterType.CUI, vals1=['NAMEFILTER1'], vals2=['CUI1']):
        tf1 = TypedFilter(type=ft1, values=vals1)
        tf2 = TypedFilter(type=ft2, values=vals2)
        dicts = TypedFilter.list_to_dicts([tf1, tf2])
        self.assertIsInstance(dicts, list)
        self.assertEqual(len(dicts), 2)
        for d in dicts:
            with self.subTest(f'Assuming dict: {d}'):
                self.assertIsInstance(d, dict)

    def test_multiple_TypedFilter_serialise_into(self, ft1=FilterType.NAME, ft2=FilterType.CUI, vals1=['NAMEFILTER1'], vals2=['CUI1']):
        tf1 = TypedFilter(type=ft1, values=vals1)
        tf2 = TypedFilter(type=ft2, values=vals2)
        dicts = TypedFilter.list_to_dicts([tf1, tf2])
        self.assertIsInstance(dicts, list)

    def test_multiple_TypedFilter_deserialise(self, ft1=FilterType.NAME, ft2=FilterType.CUI, vals1=['NAMEFILTER1'], vals2=['CUI1']):
        tf1 = TypedFilter(type=ft1, values=vals1)
        tf2 = TypedFilter(type=ft2, values=vals2)
        tf1_cp, tf2_cp = TypedFilter.from_dict(
            TypedFilter.list_to_dict([tf1, tf2]))
        self.assertIsInstance(tf1_cp, TypedFilter)
        self.assertIsInstance(tf2_cp, TypedFilter)

    def test_multiple_TypedFilter_deserialise_to_same(self, ft1=FilterType.NAME, ft2=FilterType.CUI, vals1=['NAMEFILTER1'], vals2=['CUI1']):
        tf1 = TypedFilter(type=ft1, values=vals1)
        tf2 = TypedFilter(type=ft2, values=vals2)
        the_dict = TypedFilter.list_to_dict([tf1, tf2])
        self.assertIsInstance(the_dict, dict)
        print('THE dict', the_dict)
        tf1_cp, tf2_cp = TypedFilter.from_dict(the_dict)
        self.assertEqual(tf1, tf1_cp)
        self.assertEqual(tf2, tf2_cp)
