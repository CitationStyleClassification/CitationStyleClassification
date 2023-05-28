templates = {
    'capital_letter': 'cl',
    'small_letter': 'sl',
    'uppercase_word': 'uw',
    'capitalized_word': 'cw',
    'other_word': 'ow',
    'number': 'num',
    'year': 'yr',
    'comma': ',',
    'dot': '.',
    'colon': ':',
    'semicolon': ';',
    'slash': '/',
    'left_round_bracket': '(',
    'right_round_bracket': ')',
    'left_square_bracket': '[',
    'right_square_bracket': ']',
    'ampersand': '&',
    'quote': '"',
    'defis': '-',
    'tiret': '—',
    'space': 'sp',
    'asterisk': '*',
    'minus': '–'
}


def get_symbol_name(ch: str):
    match ch:
        case '.':
            return 'dot'
        case ',':
            return 'comma'
        case ':':
            return 'colon'
        case ';':
            return 'semicolon'
        case '/':
            return 'slash'
        case '&':
            return 'ampersand'
        case '"':
            return 'quote'
        case ' ':
            return 'space'
        case '-':
            return 'defis'
        case '—':
            return 'tiret'
        case '(':
            return 'left_round_bracket'
        case ')':
            return 'right_round_bracket'
        case '[':
            return 'left_square_bracket'
        case ']':
            return 'right_square_bracket'
        case '*':
            return 'asterisk'
        case '–':
            return 'minus'


def get_word_token(word: str):
    if not word.isalpha():
        return ""
    if len(word) == 1:
        if word.isupper():
            return 'capital_letter'
        else:
            return 'small_letter'
    elif word.isupper():
        return 'uppercase_word'
    elif word[0].isupper():
        return 'capitalized_word'
    else:
        return 'other_word'


def get_number_token(word):
    if not word.isdigit():
        return ""
    if 1900 <= int(word) <= 2100 or word[0] == '0':  # or 10 <= int(word) <= 99:
        return 'year'
    else:
        return 'number'


def get_alphanum_token(word):
    if word.isalpha():
        return get_word_token(word), ""
    elif word.isdigit():
        return get_number_token(word), ""
    else:
        # Ski1993 | AGT67
        for i in range(len(word) - 1):
            if word[i].isalpha() and word[i + 1].isdigit():
                letters, digits = word[:i + 1], word[:i + 1]
                return get_word_token(letters), get_number_token(digits)
            elif word[i].isdigit() and word[i + 1].isalpha():
                digits, letters = word[:i + 1], word[i + 1:]
                return get_number_token(digits), get_word_token(letters)


def split_string(s: str):
    space_index = 0
    tokens = []

    for i in range(len(s)):
        if not s[i].isalnum():
            if space_index + 1 < i:
                result = get_alphanum_token(s[space_index + 1:i])
                tokens.append(result[0])
                tokens.append(result[1])
            space_index = i
            tokens.append(get_symbol_name(s[i]))

    if space_index + 1 < len(s):
        result = get_alphanum_token(s[space_index + 1:])
        tokens.append(result[0])
        tokens.append(result[1])

    tokens = list(filter(lambda string: string != "", tokens))
    tokens = list(filter(lambda string: string is not None, tokens))

    # print(list(tokens))

    return list(map(lambda string: templates[string], tokens))
