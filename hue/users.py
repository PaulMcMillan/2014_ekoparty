import random
import string
from itertools import product

USERNAME_PREFIX = ''
USERNAME_LENGTH = 10
CHARSET = string.octdigits


def generate_username(prefix=USERNAME_PREFIX,
                      length=USERNAME_LENGTH):
    """This generator structure lets us combine the timing attack with a
    best-effort brute force search. This gets us the best of both
    worlds...
    """
    suffix_length = length - len(prefix)
    # keep going even after we've done all the combinations, in case
    # of failure elsewhere.
    while True:
        # this shuffle is not numerically necessary assuming a truly
        # random username, but it makes people feel more comfortable
        # with the approach.
        product_input = [charset() for x in range(suffix_length)]
        for suffix in product(*product_input):
            yield prefix + ''.join(suffix)


def charset():
    """ returns the charset in a random order """
    return random.sample(CHARSET, len(CHARSET))


if __name__ == '__main__':
    # a basic check to make sure we get all combinations
    name_length = 6
    perms = generate_username('', name_length)
    for x in range(100):
        assert ''.join(random.sample(CHARSET, name_length)) in perms
    # if this never returns, the generator isn't generating all combinations
