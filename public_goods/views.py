from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    body_text = "Introduction text."
    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players payoff: How much each has earned"""

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
        }

class Results_control(Page):
    def is_displayed(self):
        if self.player.participant.treatment == 'control':
            return True
class Results_t1(Page):
    def is_displayed(self):
        if self.player.participant.treatment == 't1':
            return True
class Results_t2(Page):
    def is_displayed(self):
        if self.player.participant.treatment == 't2':
            return True

page_sequence = [
    Introduction,
    Contribute,
    ResultsWaitPage,
    Results
]
