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
2-player Hotelling location and price game. Locations fixed, and prices adjusted in by players. 
"""

class Constants(BaseConstants):
    name_in_url = 'task_02p_10t_03'
    task_timer = 5 #see Subsession, before_session_starts setting. 
    num_rounds = 36
    players_per_group = 2 
    transport_cost = 1

class Subsession(BaseSubsession):

	def before_session_starts(self):

		# randomize groups, and placement in groups
		if ((self.round_number == None) | (self.round_number == 1)):
			self.group_randomly()


			if 'period_number' in self.session.config:
			    self.session.config['period_number'] = self.session.config['period_number'] + 1
			else: 
			    self.session.config['period_number'] = 1



		# how long is the real effort task time? 
		# refer to settings.py settings. 
		for p in self.get_players():
			if 'subperiod_time' in self.session.config:
			    p.subperiod_time = self.session.config['subperiod_time']
			else:
			    p.subperiod_time = Constants.task_timer

			p.transport_cost = Constants.transport_cost

			p.period_number = self.session.config['period_number']

			if self.round_number == 1: 
				p.price = random.uniform(0, 1)

				#set loc based on player id
				if p.id_in_group == 1: 
					p.participant.vars["loc"] = 0.25
				else: p.participant.vars["loc"] = 0.75


class Group(BaseGroup):

	def set_payoffs(self):
		"""calculate payoffs in round"""

		for p in self.get_players():

			# if no price (ie price-slider unoved), get prev subperiod price
			if p.price == None:
				p.price = p.in_round(self.round_number-1).price

			# loc variable setup
			if p.participant.vars['loc'] == 0.25:
				p1_l = 0.25
				p1_p = p.price
			elif p.participant.vars['loc'] == 0.75:
				p2_l = 0.75
				p2_p = p.price

			t = p.transport_cost


		for p in self.get_players():

			# payoffs conditional on player type.
			# Calc payoff info 
			if (p.participant.vars['loc'] == 0.25):
			    intersection = ((t * p2_l) + p2_p + (t * p1_l) - p1_p) / (2*t)
			    if (intersection > 0.75):
			        pi_1 = 1 * p1_p
			        pi_2 = 0
			        boundary = 1
			        market_share = "0 to 1"
			        boundary_lo = 0
			        boundary_hi = 1
			    elif (intersection < 0.25):
			        # is p2 priced so low as to win the market?
			        pi_1 = 0
			        pi_2 = 1 * p2_p
			        boundary = 0
			        market_share = "None"
			        boundary_lo = 0
			        boundary_hi = 0 
			    else:
			        # else, they share market, 
			        # find intersection: 
			        pi_1 = p1_p * intersection
			        pi_2 = p2_p * (1 - intersection)
			        boundary = intersection
			        market_share =  "0 to " + str(boundary)
			        boundary_lo = 0
			        boundary_hi = intersection

			if (p.participant.vars['loc'] == 0.75):
			    #if I am player2:
			    intersection = ((t*p2_l) + p2_p + (t * p1_l) - p1_p) / (2*t)
			    if (intersection > 0.75):
			        pi_2 = 1 * p1_l
			        pi_1 = 0
			        boundary = 1
			        market_share = "None"
			        boundary_lo = 0
			        boundary_hi = 0
			    elif (intersection < 0.25):
			        # is p2 priced so low as to win the market?
			        pi_2 = 0
			        pi_1 = 1 * p2_p
			        boundary = 0
			        market_share = "0 to 1"
			        boundary_lo = 0
			        boundary_hi = 1
			      
			    else:
			        # else, they share market, 
			        # find intersection: 
			        pi_2 = p1_p * intersection
			        pi_1 = p2_p * (1 - intersection)
			        boundary = intersection
			        market_share = str(boundary) + " to 1 "
			        boundary_lo = intersection
			        boundary_hi = 1

			p.round_payoff = pi_1 / Constants.num_rounds / 2
			p.loc = p.participant.vars['loc']
			p.boundary_lo = boundary_lo
			p.boundary_hi = boundary_hi
			p.cumulative_round_payoff = pi_1




class Player(BasePlayer):

	period_number = models.PositiveIntegerField(
		doc='''period number'''
	)

	subperiod_time = models.PositiveIntegerField(
	    doc="""The length of the real effort task timer."""
	)

	transport_cost = models.PositiveIntegerField(
	    doc="""transport cost"""
	)

	loc = models.FloatField(
		doc="player's location")

	price = models.FloatField(
		doc="player's price")

	boundary_lo = models.FloatField(
		doc="player's low end of boundary")

	boundary_hi = models.FloatField(
		doc="player's high end of boundary")

	round_payoff = models.FloatField(
		doc="player's payoffs this round/subperiod")

	cumulative_round_payoff = models.FloatField(
		doc="player's payoffs sumulative this round/subperiod. Final round's cumulative_round_payoff is score for this period")

	paid_period = models.IntegerField(
		doc='''1 if this is a paid period, 0 otherwise''')



