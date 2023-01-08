from unittest import TestCase
from string_to_tokens import split_string, get_alphanum_token


class Test(TestCase):
    def test_get_alphanum_token(self):
        self.assertEqual(
            first=[
                'capital_letter',
                'small_letter',
                'uppercase_word',
                'capitalized_word',
                'other_word',
                'year',
                'number'
            ],
            second=[
                get_alphanum_token('A')[0],
                get_alphanum_token('b')[0],
                get_alphanum_token('UPPER')[0],
                get_alphanum_token('Capitalized')[0],
                get_alphanum_token('other')[0],
                get_alphanum_token('1965')[0],
                get_alphanum_token('339')[0]
            ]
        )

    def test_split_string_1(self):
        tokens = split_string(
            '[313] WHITLEY, D., Optimizing Neural Networks Using Genetic Algorithms, Markt and Technik, Munich, '
            'Germany, 1989. '
        )
        right_answer = [
            '[', 'number', ']', 'space', 'uppercase_word', ',', 'space', 'capital_letter', '.',
            ',', 'space', 'capitalized_word', 'space', 'capitalized_word', 'space', 'capitalized_word', 'space',
            'capitalized_word', 'space', 'capitalized_word', 'space', 'capitalized_word', ',',
            'space', 'capitalized_word', 'space', 'other_word', 'space', 'capitalized_word', ',', 'space',
            'capitalized_word', ',' 'space', 'capitalized_word', ',' 'space', 'year', '.'

        ]

        self.assertEqual(
            ''.join(tokens),
            ''.join(right_answer)
        )

    def test_split_string_2(self):
        tokens = split_string(
            '[Stupnikov(2013)] Sergey A. Stupnikov, editor. 2013. Selected Papers of the 15th All-Russian Scientific '
            'Conference "Digital libraries: Advanced Methods and Technologies, Digital Collections", Yaroslavl, '
            'Russia, October 14-17, 2013 , volume 1108 of CEUR Workshop Proceedings. CEUR-WS.org.')

        right_answer = ['[', 'capitalized_word', '(', 'year', ')', ']', 'space', 'capitalized_word', 'space',
                        'capital_letter', '.', 'space', 'capitalized_word',
                        ',', 'space', 'other_word', '.', 'space', 'year', '.', 'space', 'capitalized_word', 'space',
                        'capitalized_word', 'space', 'other_word', 'space', 'other_word', 'space', 'number',
                        'other_word',
                        'space', 'capitalized_word', '-', 'capitalized_word', 'space', 'capitalized_word', 'space',
                        'capitalized_word', 'space',
                        '"', 'capitalized_word', 'space', 'other_word', ':', 'space', 'capitalized_word', 'space',
                        'capitalized_word', 'space', 'other_word',
                        'space', 'capitalized_word', ',', 'space', 'capitalized_word', 'space', 'capitalized_word', '"',
                        ',', 'space', 'capitalized_word',
                        ',', 'space', 'capitalized_word', ',', 'space', 'capitalized_word', 'space', 'number', '-',
                        'number', ',', 'space', 'year',
                        'space', ',', 'space', 'other_word', 'space', 'number', 'space', 'other_word', 'space',
                        'uppercase_word', 'space',
                        'capitalized_word', 'space', 'capitalized_word', '.', 'space', 'uppercase_word', '-',
                        'uppercase_word', '.', 'other_word', '.']

        self.assertEqual(
            ''.join(tokens),
            ''.join(right_answer)
        )

    def test_split_string_3(self):
        tokens = split_string(
            '[15] Mayer HA, Huber R, Schwaiger R. 1996 Lean artificial neuralnetworks - regularization helps '
            'evolution. In: Alander [1], pp. 163–172. (ftp.uwasa.fics/2NWGA*.ps.Z).')
        right_answer = ['[', 'number', ']', 'space', 'capitalized_word', 'space', 'uppercase_word', ',', 'space',
                        'capitalized_word', 'space',
                        'capital_letter', ',', 'space', 'capitalized_word', 'space', 'capital_letter', '.', 'space',
                        'year', 'space', 'capitalized_word',
                        'space', 'other_word', 'space', 'other_word', 'space', '-', 'space', 'other_word', 'space',
                        'other_word', 'space',
                        'other_word', '.', 'space', 'capitalized_word', ':', 'space', 'capitalized_word', 'space', '[',
                        'number',
                        ']', ',', 'space', 'other_word', '.',
                        'space', 'number', '–', 'number', '.', 'space', '(', 'other_word', '.', 'other_word', '.',
                        'other_word', '/', 'number', 'uppercase_word', '*', '.', 'other_word',
                        '.', 'capital_letter', ')', '.']
        self.assertEqual(
            ''.join(tokens),
            ''.join(right_answer)
        )

        # TODO: написать ещё тесты!
        # TODO: затем сформировать новый датасет
