# -*- coding: cp1252 -*-
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import inflect
import random
from django.conf import settings

author = 'Lillian Chen. Special thanks to Eli Pandolfo for the basic structure, and Xiaotian Lu for initial edits.'

''' notes

'''


class Constants(BaseConstants):

    # can be changed to anything
    name_in_url = 'BaselineTask'

    # Do not change
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            # these are variable and can be set to anything by the person running the experiment.
            # 0 and 100 are the default values
            lower_bound = self.session.config.get('lower_bound')
            upper_bound = self.session.config.get('upper_bound')

            problems = []
            answers = []
            # create list of problems.
            # this is done serverside instead of clientside because everyone has the same problems, and
            # because converting numbers to words is easier in python than in JS.

            # JSON converts python tuples to JS lists, so this data structure is a list
            # of pairs, each holding a triple and its sum.
            # [ ( ('two', 'fifteen', 'forty four'), 61 )... ]

            # numbers are randomly generated between lower_bound and upper_bound, both inclusive.
            # inflect is used to convert numbers to words easily
            n2w = inflect.engine()

            # assuming no one can do more than 500 problems in 2 minutes
            # or 200
            for n in range(200):
                v1 = random.randint(lower_bound, upper_bound)
                v2 = random.randint(lower_bound, upper_bound)
                v3 = random.randint(lower_bound, upper_bound)

                answer = v1 + v2 + v3

                s1 = n2w.number_to_words(v1).capitalize()
                s2 = n2w.number_to_words(v2)
                s3 = n2w.number_to_words(v3)

                words = (s1, s2, s3)
                entry = (words, answer)

                problems.append(entry)
                answers.append(answer)

            self.session.vars['baseline_problems'] = problems
            self.session.vars['baseline_answers'] = answers

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # number of correct answers in baseline task
    baseline_score = models.IntegerField()
    baseline_bonus = models.CurrencyField()
    baseline_answers = models.StringField()
    comp_pass = models.BooleanField(initial=False)

    # number of problems attempted
    attempted = models.IntegerField()

    # arrival times
    time_Instructions = models.StringField()
    time_Baseline = models.StringField()
    time_ResultsBL = models.StringField()
    time_Survey1 = models.StringField()
    time_Comprehension = models.StringField()
    firm = models.StringField()

    # expectation question after baseline
    q1 = models.IntegerField()

    # comprehension questions for everyone
    q2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['2','3','4'],
        label='How many people will you compete against?')

    q3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['True', 'False'],
        label = '')

    q3question = models.StringField()
    q3explanation = models.StringField()


