from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """
        This is an energy game.
      """

class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'public_goods/Instructions.html'
    results_template = 'public_goods/Results_control.html'

    """Amount allocated to each player"""
    endowment = c(10)
    max_savings = c(5)
    multiplier = 1

class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        savings_session = [p.savings for p in self.get_players() if p.savings != None]
        if savings_session:
            return {
                'avg_saving': sum(savings_session)/len(savings_session),
                'min_saving': min(savings_session),
                'max_saving': max(savings_session),
            }
        else:
            return {
                'avg_saving': '(no data)',
                'min_saving': '(no data)',
                'max_saving': '(no data)',
            }
    def creating_session(self):
        treatments = itertools.cycle(['control', 't1', 't2'])
        if self.round_number == 1:
            for g in self.get_groups():
                treatment = next(treatments)
                for p in g.get_players():
                    p.participant.vars['treat'] = treatment
                    p.treat = treatment
        if self.round_number > 1 :
            for p in self.get_players():
                p.treat = p.participant.vars['treat']

class Group(BaseGroup):
    total_savings = models.CurrencyField() #
    individual_savings_share = models.CurrencyField()
    def set_payoffs(self):
        self.total_savings = sum([p.savings for p in self.get_players()])
        self.individual_savings_share = self.total_savings * Constants.multiplier / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.savings) + self.individual_savings_share

class Player(BasePlayer):
    treat = models.CharField()
    consumption = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    savings = models.CurrencyField(min=0, max=Constants.max_savings)
