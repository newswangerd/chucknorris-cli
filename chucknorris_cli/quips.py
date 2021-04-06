import random

quips = '''When Alexander Bell invented the telephone, he had three missed calls from {name}.
Fear of spiders is arachnophobia, fear of tight spaces is claustrophobia, fear of {name} is called logic.
{name} doesn't call the wrong number. You answer the wrong phone.
There used to be a street named after {name}, but it was changed because nobody crosses {name} and lives.
Ghosts sit around the campfire and tell {name} stories.
{name} has already been to Mars. That's why there are no signs of life.
{name} won American Idol using only sign language.'''

def quip(name = "Chuck Norris", number=None):
    q = quips.split('\n')

    if number is None:
        return random.choice(q).format(name=name)
    else:
        return q[number % len(q)].format(name=name)