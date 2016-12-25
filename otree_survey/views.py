# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Display(Page):

    form_model = models.Player
    form_fields = []

 
class SOETUF_PT1(Page):

    form_model = models.Player

    form_fields = [
      'q_birthYear',
      'q_gender',
      'q_emoPower'
    ]

    def before_next_page(self):
        self.player.set_payoff()


class SOETUF_PT2(Page):

    form_model = models.Player

    form_fields = [
                     'q_CT_uncomfortable',
                     'q_CT_disturbed',
                     'q_CT_worried',
                     'q_CT_satisfied',
                     'q_CT_energetic',
                     'q_CT_happiness',
                     'q_CT_aroused',
                     'q_CT_joy',
                     'q_CT_pleasure',
                     'q_CT_optimistic',
                     'q_CT_pessimistic',
                     'q_CT_sadness',
                     'q_CT_frustrated',
                     'q_CT_hopeless',
                     'q_CT_intimidated',
                     'q_CT_anger',
                     'q_CT_scared',
                     'q_CT_anxious',
                     'q_CT_fearful',
                     'q_CT_threatened',
                     'q_CT_frightened',
                     'q_CT_terrified',
                     'q_CT_irritated' 
    ]

    def before_next_page(self):
        self.player.set_payoff()

class SOETUF_PT3(Page):

    form_model = models.Player

    form_fields = [
      'q_injustice',
      'q_morality'
    ]

    def before_next_page(self):
        self.player.set_payoff()


class SOETUF_PT4(Page):

    form_model = models.Player

    form_fields = [
      'q_7',
      'q_8',
      'q_9',
      'q_10',
      'q_11',
      'q_12',
      'q_13',
      'q_14',
      'q_15'
    ]

    def before_next_page(self):
        self.player.set_payoff()


class SOETUF_PT5(Page):

    form_model = models.Player

    form_fields = [
      'q_16',
      'q_17',
      'q_18'
    ]

    # form_fields = [,

    #               # 'q_injustice',
    #               # 'q_morality',
    #               # 'q_7',
    #               # 'q_8',
    #               # 'q_9',
    #               # 'q_10',
    #               # 'q_11',
    #               # 'q_12',
    #               # 'q_13',
    #               # 'q_14',
    #               # 'q_15',
    #               # 'q_16',
    #               # 'q_17',
    #               # 'q_18',
    #               'q_BF1',
    #               'q_BF2',
    #               'q_BF3',
    #               'q_BF4',
    #               'q_BF5',
    #               'q_BF6',
    #               'q_BF7',
    #               'q_BF8',
    #               'q_BF9',
    #               'q_BF10'
    #               ]

    def before_next_page(self):
        self.player.set_payoff()

page_sequence = [
    Display,
    SOETUF_PT1,
    SOETUF_PT2,
    SOETUF_PT3,
    SOETUF_PT4,
    SOETUF_PT5
]
