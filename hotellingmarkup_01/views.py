from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time

class Intro(Page):
    timeout_seconds = 180

    form_model = models.Player

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):

        if self.round_number == 1:
            self.participant.vars['start_time'] = None

        return self.round_number == 1

    def vars_for_template(self):
        
        return {
            'round':self.round_number,
            'my_loc':self.participant.vars["loc"],
            'other_loc':self.player.get_others_in_group()[0].participant.vars["loc"],
        }

class WaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class task(Page):   


    # timeout_seconds = 10
    # timeout_submission = {'price': 1}

    form_model = models.Player
    form_fields = [
        'price',
        ]

    def after_all_players_arrive(self):
        pass

    def vars_for_template(self):

        if self.round_number == 1:
            my_prev_price = self.player.price
            other_prev_price = self.player.get_others_in_group()[0].price
        else: 
            my_prev_price = self.player.in_round(self.round_number-1).price
            other_prev_price = self.player.get_others_in_group()[0].in_round(self.round_number-1).price
       

         
        return {
            'subperiod_timer':self.player.subperiod_time,
            'transport_cost':self.player.transport_cost,
            'round':self.round_number,
            'num_rounds':Constants.num_rounds,
            'my_loc':self.participant.vars['loc'],
            'my_prev_price':my_prev_price,
            'other_prev_price':other_prev_price,
            'other_loc':self.player.get_others_in_group()[0].participant.vars["loc"],
        }



    def before_next_page(self):
        pass 


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        pass
        # for p in self.group.get_players():
        #     p.set_payoff()


class Results(Page):
    def is_displayed(self):
        self.round_number == Constants.num_rounds

    def vars_for_template(self):
        pass

page_sequence = [Intro, WaitPage, task, Results]