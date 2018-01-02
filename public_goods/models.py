from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """
        This is a one-period public goods game with 3 players.
      """

class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 25
    num_rounds = 12

    instructions_template = 'public_goods/Instructions.html'
    results_template = 'public_goods/Results_control.html'

    """Amount allocated to each player"""
    endowment = c(10)
    multiplier = 1

class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution != None]
        if contributions:
            return {
                'avg_contribution': sum(contributions)/len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
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
    total_contribution = models.CurrencyField() #
    individual_share = models.CurrencyField()
    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    treat = models.CharField()
    # Savings
    # consumptions
