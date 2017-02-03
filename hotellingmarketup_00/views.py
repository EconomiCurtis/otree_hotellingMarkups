from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, check_and_ok
from django.conf import settings
import time
import random

class holdon(Page):
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        return {
            'charityinfo':self.player.charity_info,
            'gender_setting_female':self.player.gender_setting_female,
            'homog':self.player.homog,
        }


class Init(Page):

  
    form_model = models.Player
    form_fields = [
    'subject_email',
    'subject_done_before',
    ]

    def is_displayed(self):

        if self.round_number == 1:
            self.participant.vars['start_time'] = None
        return self.round_number == 1
    
    def subject_email_error_message(self, value):
        if ("@zu.ac.ae" not in value)&("@ZU.AC.AE" not in value):
            return 'Must contain a valid ZU email address, for example 201112345@zu.ac.ae.'

    def vars_for_template(self):
        return {
            'charityinfo':self.player.charity_info,
            'gender_setting_female':self.player.gender_setting_female,
            'homog':self.player.homog,
        }

class Intro1(Page):
    # timeout_seconds = 300

    def is_displayed(self):

        if self.round_number == 1:
            self.participant.vars['start_time'] = None

        return self.round_number == 1
    
    def vars_for_template(self):
        return {
            'charityinfo':self.player.charity_info,
            'gender_setting_female':self.player.gender_setting_female,
            'homog':self.player.homog,
        }

class Intro2(Page):
    timeout_seconds = 180

    def is_displayed(self):
        return self.round_number < 2




page_sequence = [
    holdon,
    Init,
    Intro1,
    ]






