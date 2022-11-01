from unittest import TestCase
import re


def onlyDigits(s):
    for ch in s:
        if ch not in '1234567890':
            return False
    return True


def onlyLetters(s):
    for ch in s:
        if ch.lower() not in 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            return False
    return True


def begin_ref(s):
    begin = s[s.find('[') + 1: s.find(']')]
    '''
    [1] - #1
    [Ackley85]  - #2
    [Ackley(1985)] - #3
    [Yae] - #4
    [Ackley, 1985] - #5
    [Ackley 1985] - #6
    [A Connectionist Algorithm for Genetic SearchAckley1985] - #7
    [] - #8 (стиль namunsrt)
    [Ackley 85] - #9
    [Ackl 85] - #10 (фамилия автора сокращена до 4 букв)
    [Ackley1985], [Alba, Aldana, and TroyaAlba et al.1993] - #11
    '''
    if not begin:
        return 8
    elif begin.count(':') == 2:
        return 12
    elif onlyDigits(begin):
        return 1
    elif onlyLetters(begin) or re.fullmatch(r'[a-zA-Z.]+\d?', begin):  # onlyLetters(begin):
        return 4
    elif '(' in begin:
        return 3
    elif re.fullmatch(r'[a-zA-Z]{4} \d\d[a-zA-Z]*', begin):
        return 10
    elif re.fullmatch(r'[a-zA-Z.& ]+, \d{4}[a-zA-Z]?', begin):
        return 5
    elif re.fullmatch(r'[a-zA-Z. ]+\s\d{4}', begin):
        return 6
    elif re.fullmatch(r'[a-zA-Z,. ]+\d{4}[a-zA-Z]?', begin):
        return 11
    elif re.fullmatch(r'[a-zA-Z]+\d\d[a-zA-Z]*', begin):
        return 2
    elif re.fullmatch(r'[a-zA-Z]+ \d\d[a-zA-Z]*', begin):
        return 9
    else:
        return 7


class Test(TestCase):
    def test1(self):
        self.assertEqual(1, begin_ref('[1]'))

    def test2(self):
        self.assertEqual(
            (2, 2, 2, 2, 2),
            (begin_ref('[Ackley85]'), begin_ref('[AAT93]'), begin_ref('[ACFX93]'), begin_ref('[Ack85]'),
             begin_ref('[Bel89a]'))
        )

    def test3(self):
        self.assertEqual(
            (3, 3, 3, 3, 3),
            (
                begin_ref('[Ackley(1985)]'),
                begin_ref('[Ackley & Littman(1992)]'),
                begin_ref('[Alba et al.(1993)Alba, Aldana & Troya]'),
                begin_ref('[Belew(1989b)]'),
                begin_ref('[Zhang and Veenker(1991)]')
            )
        )

    def test4(self):
        self.assertEqual(
            (4, 4, 4, 4, 4),
            (begin_ref('[Yae]'), begin_ref('[Wie2]'), begin_ref('[WO]'), begin_ref('[WDDA]'), begin_ref('[G.M]'))
        )

    def test5(self):
        self.assertEqual(
            (5, 5, 5, 5),
            (begin_ref('[Ackley, 1985]'), begin_ref('[Ackley & Littman, 1992]'), begin_ref(' [Alba et al., 1993]'),
             begin_ref('[Belew, 1989a]'))
        )

    def test6(self):
        self.assertEqual(
            (6, 6),
            (begin_ref('[Ackley 1985]'), begin_ref('[Ackley . Littman 1992]'))
        )

    '''def test7(self):
        self.assertEqual(
            (7,),
            (begin_ref('[A Connectionist Algorithm for Genetic SearchAckley1985]'),)
        )
    '''

    def test8(self):
        self.assertEqual(
            (8,),
            (begin_ref('[]'),)
        )

    def test9(self):
        self.assertEqual(
            (9, 9, 9),
            (begin_ref('[Grefenstette 87]'), begin_ref('[Ackley 85]'), begin_ref('[Gruau 92b]'))
        )

    def test10(self):
        self.assertEqual(
            (10, 10),
            (begin_ref('[Ackl 85]'), begin_ref('[Bele 89a]'))
        )

    def test11(self):
        self.assertEqual(
            (11, 11, 11, 11, 11, 11),
            (
                begin_ref('[Ackley1985]'),
                begin_ref('[Alba, Aldana, and TroyaAlba et al.1993]'),
                begin_ref('[Belew et al.1990]'),
                begin_ref('[Bergman1988]'),
                begin_ref('[Chang and Lippmann1991]'),
                begin_ref('[de Garis1990a]')
            )
        )

    def test12(self):
        self.assertEqual(
            (12, 12, 12),
            (
                begin_ref('[Abelson:1985:SIC]'),
                begin_ref('[Agre:1988:WP]'),
                begin_ref('[Ambroszkiewicz:1995:KBM]')
            )
        )
