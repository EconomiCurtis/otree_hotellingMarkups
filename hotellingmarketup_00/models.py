# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
# </standard imports>

author = 'Curtis Kephart'

doc = """
An implementation of Niederle Vesterlund real effort task in oTree.
Subjects add up sets of five two-digit numbers. 
Numbers are randomly drawn. 
Once the participant submits an answer on the computer, a new problem appears jointly with information on whether the former answer was correct.
The final score is determined by the number of correctly solved problems. 
"""

def check_and_ok(user_total, reference_ints):
    ok = (user_total == sum(reference_ints))
    return ok

class Constants(BaseConstants):
    name_in_url = 'intro_1p'
    players_per_group = None
    num_rounds = 1
    charityInfo = True #true implies mention charity/giving and have reminders for charity
    gender_setting_female = True  # True implies female
    homog = True  #true means compare to people who played agains only the same sex. 

class Subsession(BaseSubsession):

    def before_session_starts(self):

        # how long is the real effort task time? 
        # refer to settings.py settings. 
        for p in self.get_players():
            if 'Treatment_Charity_info' in self.session.config:
                p.charity_info = self.session.config['Treatment_Charity_info']
            else:
                p.charity_info = Constants.charityInfo #true implies mention charity/giving and have reminders for charity

        for p in self.get_players():
            if 'gender_setting_female' in self.session.config:
                p.gender_setting_female = self.session.config['gender_setting_female']
            else:
                p.gender_setting_female = Constants.gender_setting_female # True implies female

        for p in self.get_players():
            if 'homog' in self.session.config:
                p.homog = self.session.config['homog']
            else:
                p.homog = Constants.homog # T true means compare to people who played agains only the same sex. 



class Group(BaseGroup):
	pass



class Player(BasePlayer):

    charity_info = models.BooleanField(
        doc="Treatment, are subjects given charity info in instructions?")

    gender_setting_female = models.BooleanField(
        doc="Treatment, are subjects female? ie, from a female class")

    homog = models.BooleanField(
        doc="Treatment, are subjects compared to the same sex-group (all females or all males) or a mix?")


    subject_done_before = models.CharField(
        doc = 'did this subject do this experiment before?',
        initial=None,
        choices=['Yes','No'],
        verbose_name='Have you participated in this experiment before?',
        widget=widgets.RadioSelect())


    subject_email = models.CharField(
        doc = 'subject email',
        verbose_name='Please enter your <b>Zayed University</b> email address <font color="gray"><br>for example, 201112345@zu.ac.ae</font>',
        )

    subject_name = models.CharField(
        doc = 'subject name',
        verbose_name='Please enter your name.',
        )



