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
        yield (pages.Instructions, {'time_Instructions': 'test'})
        yield Submission(pages.Baseline, 
            {'time_Baseline': 'test', 'baseline_score': score, 'attempted': att}, 
            check_html=False)
        yield (pages.ResultsBL, {'time_ResultsBL': 'test'})
        yield (pages.Survey1, {'time_Survey1': 'test', 'q1': 5})
