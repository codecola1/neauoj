__author__ = 'Code_Cola'

from access import Access
from status.models import Solve


class Vjudge:
    def __init__(self, sid):
        solve = Solve.objects.get(id=sid)
