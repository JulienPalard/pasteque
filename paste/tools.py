from string import digits, ascii_uppercase
from random import choice, choices
import shortuuid
import os
from webtools import settings


def random_id(model):
    """Returns a short uuid for the slug of the given model.

    If a DICT is given in the settings, try to use it to generate
    nicer URLS like:
    """
    pool = digits + ascii_uppercase
    slug = choice(digits) + choice(ascii_uppercase) + "-" + "".join(choices(pool, k=2))
    if not model.objects.filter(slug=slug):
        return slug
    # fallback to the shortuuid strategy:
    uuid = choice("0123456789") + shortuuid.uuid()
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
