# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

from django_countries.fields import CountryField
from django.utils.html import escape





class Constants(BaseConstants):
    name_in_url = 'otree_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0


#section 1
    q_birthYear = models.PositiveIntegerField(
        verbose_name='What year were you born?',
        min = 1900,
        max = 2016,
        initial=None)

    # q_gender = models.CharField(
    #     initial=None,
    #     choices=['Female','Male','Other'],
    #     verbose_name='What gender are <b>you?</b>',
    #     widget=widgets.RadioSelect())

    q_gender = models.CharField(
        initial=None,
        choices=['Female','Male','Other'],
        verbose_name='What gender are <b>you ?</b>   What gender are &lt;b&gt;you ?&lt;/b&gt;',
        help_text='What gender are <b>you ?</b>',
        widget=widgets.RadioSelect())

    q_emoPower = models.IntegerField(
        initial=None,
        choices=[
            [4, 'Very Strong'],
            [3, 'Strong'],
            [2, 'Moderate'],
            [1, 'Weak'],
            [0, 'Not at All']
        ],
        verbose_name='How emotionally powerful was this story to you?',
        widget=widgets.RadioSelect())

    ## Choice Table
    ChoiceTable1 = {
                     'q_CT_uncomfortable':'uncomfortable',
                     'q_CT_disturbed':'disturbed',
                     'q_CT_worried':'worried',
                     'q_CT_satisfied':'satisfied',
                     'q_CT_energetic':'energetic',
                     'q_CT_happiness':'happiness',
                     'q_CT_aroused':'aroused',
                     'q_CT_joy':'joy',
                     'q_CT_pleasure':'pleasure',
                     'q_CT_optimistic':'optimistic',
                     'q_CT_pessimistic':'pessimistic',
                     'q_CT_sadness':'sadness',
                     'q_CT_frustrated':'frustrated',
                     'q_CT_hopeless':'hopeless',
                     'q_CT_intimidated':'intimidated',
                     'q_CT_anger':'anger',
                     'q_CT_scared':'scared',
                     'q_CT_anxious':'anxious',
                     'q_CT_fearful':'fearful',
                     'q_CT_threatened':'threatened',
                     'q_CT_frightened':'frightened',
                     'q_CT_terrified':'terrified',
                     'q_CT_irritated':'irritated'               
    } #see for loop below class

    q_injustice = models.IntegerField(
        initial=None,
        choices=[
            [4, 'Very Strong'],
            [3, 'Strong'],
            [2, 'Moderate'],
            [1, 'Weak'],
            [0, 'Not at All']
        ],
        verbose_name='To what degree did the story arouse a ‘sense of injustice’ within you?',
        widget=widgets.RadioSelect())

    q_morality = models.IntegerField(
        initial=None,
        choices=[
            [4, 'Very Strong'],
            [3, 'Strong'],
            [2, 'Moderate'],
            [1, 'Weak'],
            [0, 'Not at All']
        ],
        verbose_name='To what degree did the story violate your ‘sense of morality’?',
        widget=widgets.RadioSelect())

    ## Choice Table 2
    ChoiceTable2 = {
                     'q_7':'Subjects in the study were forced into participation.',
                     'q_8':'Subjects in the study were coerced (‘pressured’?) into joining the study against their best interests.',
                     'q_9':'Coercion (“pressure”?) was used on subjects, once they were in the study, to remain in the study until it was over?',
                     'q_10':'The investigators ‘did good’, overall, to the subjects in the study.',
                     'q_11':'Despite their best intentions, the investigators failed to ‘do good’ for the subjects in the study.',
                     'q_12':'The investigators never intend to ‘do good’ for the study subjects.',
                     'q_13':'The investigators ‘did no harm’ at all to the subjects in the study at all.',
                     'q_14':'The investigators seemed to have inadvertently caused ‘harm’ to a few study subjects.',
                     'q_15':'The investigators appear to have planned to ‘do harm’ to the study subjects and had no concern about doing that.'
                    }
                     

    # 16-18: While all elements of society may have benefitted from the findings of the study, … 
    ChoiceTable3 = {
                     'q_16':'…all levels of society (the rich and powerful as well as the poor and vulnerable) were equally recruited into the study.',
                     'q_17':'...the poor and vulnerable in society were much more strongly recruited into the study.',
                     'q_18':'...only the poor and vulnerable were recruited into the study.'
                    }
                     


#     q_16 = models.CharField(
#         initial=None,
#         choices=['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree', 'Don’t Know'],
#         verbose_name='…all levels of society (the rich and powerful as well as the poor and vulnerable) were equally recruited into the study.',
#         widget=widgets.RadioSelect())

#     q_17 = models.CharField(
#         initial=None,
#         choices=['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree', 'Don’t Know'],
#         verbose_name='...the poor and vulnerable in society were much more strongly recruited into the study.',
#         widget=widgets.RadioSelect())

#     q_18 = models.CharField(
#         initial=None,
#         choices=['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree', 'Don’t Know'],
#         verbose_name='...only the poor and vulnerable were recruited into the study',
#         widget=widgets.RadioSelect())


#     crt_bat = models.PositiveIntegerField()
#     crt_widget = models.PositiveIntegerField()
#     crt_lake = models.PositiveIntegerField()

         #Big Five
for key in Player.ChoiceTable1:
    Player.add_to_class(key,
        models.IntegerField(initial=None,
        # choices=[
        #     [4, 'Very Strong'],
        #     [3, 'Strong'],
        #     [2, 'Moderate'],
        #     [1, 'Weak'],
        #     [0, 'Not at All']
        # ],
        choices=[
            [4, ''],
            [3, ''],
            [2, ''],
            [1, ''],
            [0, '']
        ],
        verbose_name = Player.ChoiceTable1[key],
        widget=widgets.RadioSelectHorizontal())
                                             )

for key in Player.ChoiceTable2:
    Player.add_to_class(key,
        models.CharField(initial=None,
        choices=[
            ['SA', 'Strongly Agree'],
            ['A', 'Agree'],
            ['D', 'Disagree'],
            ['SD', 'Strong Disagree'],
            ['DK', "Don't Know"]
        ],
        verbose_name = Player.ChoiceTable2[key],
        widget=widgets.RadioSelectHorizontal())
                                             )

for key in Player.ChoiceTable3:
    Player.add_to_class(key,
        models.CharField(initial=None,
        choices=[
            ['SA', 'Strongly Agree'],
            ['A', 'Agree'],
            ['D', 'Disagree'],
            ['SD', 'Strong Disagree'],
            ['DK', "Don't Know"]
        ],
        verbose_name = Player.ChoiceTable3[key],
        widget=widgets.RadioSelectHorizontal())
                                             )
