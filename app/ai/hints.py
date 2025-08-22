hint_rules = {
    'gravity': 'Hint: Think about Newton’s Law of Universal Gravitation.',
    'photosynthesis': 'Hint: This process happens in chloroplasts.',
    'electricity': 'Hint: Remember Ohm’s Law and current formulas.',
     # Python-related hints
    'print': 'Hint: The print() function outputs data to the console.',
    '**': 'Hint: ** is the exponentiation operator in Python.',
    'function': 'Hint: Functions in Python are defined using the "def" keyword.',
    'tuple': 'Hint: Tuples are immutable, unlike lists.',
    'type': 'Hint: Use type() to check the data type of a value.',
    'try-except': 'Hint: Used for error handling in Python.',
    '//': 'Hint: // performs integer (floor) division.',
    '#': 'Hint: Use # to write a single-line comment in Python.',
    'class': 'Hint: Classes define new object types using the "class" keyword.',
    're': 'Hint: Python "re" module handles regular expressions.'
}

def get_hint(question_text):
    for keyword, hint in hint_rules.items():
        if keyword.lower() in question_text.lower():
            return hint
    return "No hint available. Try your best!"
