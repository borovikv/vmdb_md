import re
import time

__author__ = 'vladimir'


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.elapsed = time.time() - self._startTime


def flatten(listOfLists):
    # Flatten one level of nesting
    #return chain.from_iterable(listOfLists)
    return [item for sublist in listOfLists for item in sublist]


def is_url(word):
    """

    :rtype : bool
    """
    url_pattern = re.compile(r'^(?:http|ftp)s?://'  # http:// or https://
                             r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
                             r'localhost|'  #localhost...
                             r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                             r'(?::\d+)?'  # optional port
                             r'(?:/?|[/?]\S+)$',
                             re.IGNORECASE)
    return bool(url_pattern.match(word))


def is_email(word):
    email_pattern = re.compile(r'^[a-z0-9_.-]+@[a-z0-9_-]+\.[a-z]{3}$', re.U)
    return bool(email_pattern.match(word))


def get_obj_or_none(model, *args, **kwargs):
    obj = model.objects.filter(**kwargs)
    return obj and obj[0] or None