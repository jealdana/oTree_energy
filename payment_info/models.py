from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
    This application provides introductions for the experiment.
"""

class Constants(BaseConstants):
    name_in_url = 'exp_info'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    q1 = models.CharField()
    q2 = models.IntegerField()

