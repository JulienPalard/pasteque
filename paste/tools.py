import string
import shortuuid
import os
from webtools import settings


def next_slug(slug):
    """Returns the shortest next slug alphabetically."""
    slug = list(slug[::-1])
    for i in range(len(slug)):
        pos = string.ascii_letters.find(slug[i]) + 1
        slug[i] = string.ascii_letters[pos % 52]
        if slug[i] != 'a':
            break
    if slug[i] == 'a':
        slug.append('a')
    return "".join(slug)[::-1]


def random_id():
    """Returns an id."""
    return shortuuid.uuid()


def cache_get_filepath(key):
    """Returns cache path."""
    return os.path.join(settings.CACHE_PATH, key)


def cache_exists(key):
    """Says if cache exists for key."""
    return os.path.isfile(cache_get_filepath(key))


def cache_store(key, value):
    """Store cache value for key."""
    with open(cache_get_filepath(key), 'w') as cache_file:
        cache_file.write(value.encode('utf-8'))


def cache_fetch(key):
    """Fetch cache value for key."""
    with open(cache_get_filepath(key), 'r') as cache_file:
        return cache_file.read()
