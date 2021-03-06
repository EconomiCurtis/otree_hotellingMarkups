from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time

class Intro(Page):
    # timeout_seconds = 180

    form_model = models.Player

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):

        if self.round_number == 1:
            self.participant.vars['start_time'] = None


        return self.round_number == 1

    def vars_for_template(self):
        
        return {
            'treatment_t':self.player.transport_cost,
            'round':self.round_number,
            'my_loc':self.participant.vars["loc"],
            'other_loc':self.player.get_others_in_group()[0].participant.vars["loc"],
            'debug':settings.DEBUG,
        }

class WaitPage1(WaitPage):

    def is_displayed(self):
        return self.round_number == 1




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

        subperiod_timer = self.player.subperiod_time

        if self.round_number == 1: #initial price randomized in models subsession
            my_prev_price = self.player.price
            other_prev_price = self.player.get_others_in_group()[0].price
            cumulative_round_payoff = 0
        else: 
            my_prev_price = self.player.in_round(self.round_number-1).price #else pull price from previous round. 
            other_prev_price = self.player.get_others_in_group()[0].in_round(self.round_number-1).price


            # cumulative_round_payoff = 0
            # for p in self.player.in_all_rounds():
            #     if (p.round_payoff != None:
            #         cumulative_round_payoff = cumulative_round_payoff + p.round_payoff
            cumulative_round_payoff = sum([p.round_payoff for p in self.player.in_all_rounds() if (p.round_payoff != None)])
         
        return {
            'subperiod_timer':subperiod_timer,
            'transport_cost':self.player.transport_cost,
            'round':self.round_number,
            'num_rounds':Constants.num_rounds,
            'my_loc':self.player.loc,
            'my_prev_price':my_prev_price,
            'other_prev_price':other_prev_price,
            'other_loc':self.player.get_others_in_group()[0].loc,
            'cumulative_round_payoff':round(cumulative_round_payoff * 100, 3),
            'debug':settings.DEBUG,
        }


class WaitPage(WaitPage):

    def after_all_players_arrive(self):
        #calc payoffs and stuff
        self.group.set_payoffs() 


class ResultsWaitPage(WaitPage):

    def is_displayed(self):

        # if we don't have a log yet, (that is, we're in period one), then start a new log. 
        # save info from this round needed to calc final payoffs.       
        if self.round_number == (Constants.num_rounds):
            if 'exp_log' in self.participant.vars: #just error handling
              exp_log  = self.participant.vars['exp_log']
            else:
              exp_log = []

            cumulative_round_payoff = sum([p.round_payoff for p in self.player.in_all_rounds() if (p.round_payoff != None)])
            row = {
                'period_num':(len(exp_log) + 1),
                'period_score':round(cumulative_round_payoff * 100,6),
                'paid_period':True,
            }

            if (len(exp_log) + 1) == self.player.period_number:
                exp_log.append(row)
                self.participant.vars['exp_log'] = exp_log

        return self.round_number == (Constants.num_rounds)



class Results(Page):

    def is_displayed(self):
        return self.round_number == (Constants.num_rounds)

    def vars_for_template(self):

        cumulative_round_payoff = sum([p.round_payoff for p in self.player.in_all_rounds() if (p.round_payoff != None)])

        return{
            'debug':settings.DEBUG,
            'cumulative_round_payoff':round(cumulative_round_payoff * 100, 3),
            'exp_log':self.participant.vars['exp_log'],
        }




page_sequence = [
        Intro, 
        WaitPage1, 
        task, WaitPage,  
        ResultsWaitPage, Results
    ]









