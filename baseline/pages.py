from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
import inflect
from django.conf import settings


# overall instructions & baseline instructions
class General(Page):

    def vars_for_template(self):

        self.player.baseline_answers = ', '.join(str(x) for x in self.session.vars['baseline_answers'])
        return {
            'problems': self.session.vars['baseline_problems'],
            'answers': self.session.vars['baseline_answers'],
            'pageTimeoutWording': self.session.config.get('pageTimeoutWording')
        }


class Instructions(Page):
    form_model = 'player'
    form_fields = ['time_Instructions']

    def vars_for_template(self):
        return {
            'gameDuration': self.session.config.get('gameDuration')
        }


# baseline task
class Baseline(Page):
    form_model = 'player'
    form_fields = ['baseline_score', 'attempted', 'time_Baseline']
    timeout_seconds = settings.SESSION_CONFIGS[0]['time_limit']

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'problems': self.session.vars['baseline_problems'],
            'answers': self.session.vars['baseline_answers']
        }

    # is called after the timer runs out and this page's forms are submitted
    # sets the participant.vars to transfer to next round
    def before_next_page(self):
        self.player.participant.vars['baseline_attempted'] = self.player.attempted
        self.player.participant.vars['baseline_score'] = self.player.baseline_score
        self.player.baseline_bonus = 0.05 * self.player.baseline_score
        self.player.payoff = self.player.baseline_bonus
        self.player.participant.vars['baseline_bonus'] = self.player.payoff
        # print(self.player.payoff)


# baseline results
class ResultsBL(Page):

    form_model = 'player'
    form_fields = ['time_ResultsBL']

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'baseline_bonus': c(self.participant.payoff),
            # automatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted),
            'gameDuration': self.session.config.get('gameDuration')
        }


class Survey1(Page):
    form_model = 'player'
    form_fields = ['time_Survey1', 'q1']


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['time_Comprehension', 'q2', 'q3']

    def vars_for_template(self):
        # set firm based on session config
        self.player.firm = self.session.config['condition']
        if self.player.firm == "A":
            self.player.q3question = "True or False: I will be shown the scores my opponents obtained in part 1 " \
                                     "before entering the competition."
            self.player.q3explanation = "Each participant will be shown the scores his/her opponents " \
                                        "obtained in part 1 before entering the competition."
        if self.player.firm == "B":
            self.player.q3question = "True or False: I will not know the scores my opponents obtained in part 1 " \
                                     "before entering the competition."
            self.player.q3explanation = "Each participant knows their own score from part 1, but does not know " \
                                        "the scores his/her opponents obtained before entering the competition."
        return {
            'firm': self.player.firm,
            'q3Question': self.player.q3question,
            'q3Explanation': self.player.q3explanation,
            'gameDuration': self.session.config.get('gameDuration')
        }

    def before_next_page(self):
        if self.player.q2 == "2" and self.player.q3 == "True":
            self.player.comp_pass = True


class CompResults(Page):
    pass


class CopyMturkCode(Page):

    def is_displayed(self):
        # if comp_pass is false, it shows this page
        # the page does not allow them to continue to game 1
        return not self.player.comp_pass


# sequence in which pages are displayed
page_sequence = [
    General,
    Instructions,
    Baseline,
    ResultsBL,
    Survey1,
    Comprehension,
    CompResults,
    CopyMturkCode
]