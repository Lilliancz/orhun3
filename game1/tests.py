from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random as r


class PlayerBot(Bot):

    def play_round(self):
        score = r.randint(0,5)
        att = score + r.randint(0,5)
        yield Submission(pages.Game1, 
            {'time_Game1': 'test', 'game1_score': score, 'attempted': att},
            check_html=False)
        yield (pages.Results1, {'time_Results1': 'test'})
