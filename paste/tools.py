import string
import random
import shortuuid
import os
import re
from webtools import settings
from functools import lru_cache
from .models import Paste


@lru_cache()
def find_words():
    if not settings.DICT:
        return None
    short_words = []
    try:
        with open(settings.DICT) as dictionary:
            for line in dictionary:
                line = line.strip()
                if re.match("[a-z]{2,5}$", line):
                    short_words.append(line)
        return short_words
    except FileNotFoundError:
        return None


def random_id(model):
    """Returns a short uuid for the slug of the given model.

    If a DICT is given in the settings, try to use it to generate nicer URLS like:
    """
    short_words = find_words()
    if short_words:
        slug = (
            random.choice(string.digits)
            + random.choice(string.ascii_uppercase)
            + "-"
            + random.choice(short_words)
        )
        if not model.objects.filter(slug=slug):
            return slug
        # else, fallback to the shortuuid strategy:
    uuid = random.choice("0123456789") + shortuuid.uuid()
    for i in range(3, len(uuid)):
        potential_uuid = uuid[:i]
        if not model.objects.filter(slug=potential_uuid):
            return potential_uuid
    return uuid


def cache_get_filepath(key):
    """Returns cache path."""
    return os.path.join(settings.CACHE_PATH, key)


def cache_exists(key):
    """Says if cache exists for key."""
    return os.path.isfile(cache_get_filepath(key))


def cache_store(key, value):
    """Store cache value for key."""
    with open(cache_get_filepath(key), "w") as cache_file:
        cache_file.write(value)


def cache_fetch(key):
    """Fetch cache value for key."""
    with open(cache_get_filepath(key), "r") as cache_file:
        return cache_file.read()
