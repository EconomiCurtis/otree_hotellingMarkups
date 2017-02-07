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

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


author = 'Curtis Kephart'

doc = """
Hotelling 4-player game, locations fixed and players set prices. Discrete time. 
"""

class Constants(BaseConstants):
	name_in_url = 'task_4p_025t_06'
	subperiod_time = 5 #see Subsession, before_session_starts setting. 
	num_rounds = 20
	players_per_group = 4
	transport_cost = 0.25
	p1_loc = 0.125
	p2_loc = 0.375
	p3_loc = 0.625
	p4_loc = 0.875
	paid_period = True

class Subsession(BaseSubsession):

	def before_session_starts(self):

		# randomize groups, and placement in groups
		if ((self.round_number == None) | (self.round_number == 1)):
			self.group_randomly()

			if 'period_number' in self.session.config:
				self.session.config['period_number'] = self.session.config['period_number'] + 1
			else: 
				self.session.config['period_number'] = 1

			for p in self.get_players():
				if 'p1_loc' in self.session.config:
					p.participant.vars['p1_loc'] = self.session.config['p1_loc']
				else:
					p.participant.vars['p1_loc'] = Constants.p1_loc

				if 'p2_loc' in self.session.config:
					p.participant.vars['p2_loc'] = self.session.config['p2_loc']
				else:
					p.participant.vars['p2_loc'] = Constants.p2_loc

				if 'p3_loc' in self.session.config:
					p.participant.vars['p3_loc'] = self.session.config['p3_loc']
				else:
					p.participant.vars['p3_loc'] = Constants.p3_loc

				if 'p4_loc' in self.session.config:
					p.participant.vars['p4_loc'] = self.session.config['p4_loc']
				else:
					p.participant.vars['p4_loc'] = Constants.p4_loc



		# how long is the real effort task time? 
		# refer to settings.py settings. 
		for p in self.get_players():

			p.period_number = self.session.config['period_number']
			p.transport_cost = Constants.transport_cost
			
			# variable setup
			if p.id_in_group == 1:
				p.loc = p.participant.vars["loc"] = p.participant.vars['p1_loc']
			elif p.id_in_group == 2:
				p.loc = p.participant.vars["loc"] = p.participant.vars['p2_loc']
			elif p.id_in_group == 3:
				p.loc = p.participant.vars["loc"] = p.participant.vars['p3_loc']
			elif p.id_in_group == 4:
				p.loc = p.participant.vars["loc"] = p.participant.vars['p4_loc']


			if 'paid_period' in self.session.config:
				p.paid_period = p.participant.vars['paid_period'] = self.session.config['paid_period']

			else:
				p.paid_period = p.participant.vars['paid_period'] = Constants.paid_period


			if 'subperiod_time' in self.session.config:
				p.subperiod_time = self.session.config['subperiod_time']
			else:
				p.subperiod_time = Constants.task_timer



			if self.round_number == 1: 
				p.price = random.uniform(0, 1)



class Group(BaseGroup):

	def set_payoffs(self):
		"""calculate payoffs in round"""

		for p in self.get_players():

			# if no price (ie price-slider unoved), get prev subperiod price
			if p.price == None:
				p.price = p.in_round(self.round_number-1).price

			# variable setup
			if p.id_in_group == 1:
				p1_l = p.loc
				p1_p = p.price
			elif p.id_in_group == 2:
				p2_l = p.loc
				p2_p = p.price
			elif p.id_in_group == 3:
				p3_l = p.loc
				p3_p = p.price
			elif p.id_in_group == 4:
				p4_l = p.loc
				p4_p = p.price

			t = p.transport_cost



		# //p1 - priced out of market
		intersection_1_2 = (t * p2_l+p2_p + t * p1_l - p1_p) / (2*t)
		intersection_1_3 = (t * p3_l+p3_p + t * p1_l - p1_p) / (2*t)
		intersection_1_4 = (t * p4_l+p4_p + t * p1_l - p1_p) / (2*t)

		if ((intersection_1_2 < p1_l) | (intersection_1_3 < p1_l) | (intersection_1_4 < p1_l)):
			p1_boundary_lo = 0 
			p1_boundary_hi = 0 

		# //p4 - priced out of market
		intersection_1_4 = (t *p4_l+p4_p + t * p1_l - p1_p) / (2*t)
		intersection_2_4 = (t *p4_l+p4_p + t * p2_l - p2_p) / (2*t)
		intersection_3_4 = (t *p4_l+p4_p + t * p3_l - p3_p) / (2*t)

		if ((intersection_3_4 > p4_l) | (intersection_2_4 > p4_l) | (intersection_1_4 > p4_l)):
			p4_boundary_lo = 0 
			p4_boundary_hi = 0 

		# //p2 - priced out of market
		intersection_1_2 = (t *p2_l+p2_p + t * p1_l - p1_p) / (2*t)
		intersection_2_3 = (t *p3_l+p3_p + t * p2_l - p2_p) / (2*t)
		intersection_2_4 = (t *p4_l+p4_p + t * p2_l - p2_p) / (2*t)

		if ((intersection_1_2 > p2_l) | (intersection_2_3 < p2_l) | (intersection_2_4 < p2_l)):
			p2_boundary_lo = 0 
			p2_boundary_hi = 0

		# //p3 - priced out of market
		intersection_1_3 = (t *p3_l+p3_p + t * p1_l - p1_p) / (2*t)
		intersection_2_3 = (t *p3_l+p3_p + t * p2_l - p2_p) / (2*t)
		intersection_3_4 = (t *p4_l+p4_p + t * p3_l - p3_p) / (2*t)

		if ((intersection_1_3 > p3_l) | (intersection_2_3 > p3_l) | (intersection_3_4 < p3_l)):
			p3_boundary_lo = 0 
			p3_boundary_hi = 0 



		# //p1
		if ((intersection_1_2 < p1_l) | (intersection_1_3 < p1_l) | (intersection_1_4 < p1_l)):
			p1_boundary_lo = 0 
			p1_boundary_hi = 0 
		elif (intersection_1_2 > p2_l):
			if (intersection_1_3 > p3_l):
				if (intersection_1_4 > p4_l): #//prices below all else
					p1_boundary_lo = 0 
					p1_boundary_hi = 1 
				else:
					p1_boundary_lo = 0 
					p1_boundary_hi = intersection_1_4
			elif (intersection_1_4 < intersection_1_3): # // if p4 priced out p3!
				p1_boundary_lo = 0 
				p1_boundary_hi = intersection_1_4 
			else:
				p1_boundary_lo = 0 
				p1_boundary_hi = intersection_1_3 
		elif ((intersection_1_4 < intersection_1_3) & (intersection_1_4 < intersection_1_2)):
				p1_boundary_lo = 0 
				p1_boundary_hi = intersection_1_4 
		elif (intersection_1_3 < intersection_1_2):
				p1_boundary_lo = 0 
				p1_boundary_hi = intersection_1_3 
		else:
			p1_boundary_lo = 0 
			p1_boundary_hi = intersection_1_2


		# //p4
		if ((intersection_3_4 > p4_l) | (intersection_2_4 > p4_l) | (intersection_1_4 > p4_l)):
			p4_boundary_lo = 0 
			p4_boundary_hi = 0 
		elif (intersection_3_4 < p3_l):
			if (intersection_2_4 < p2_l):
				if (intersection_1_4 < p1_l): #//prices below all else
					p4_boundary_lo = 0 
					p4_boundary_hi = 1 
				else:
					p4_boundary_lo = intersection_1_4 
					p4_boundary_hi = 1 
			elif (intersection_1_4 > intersection_2_4): #// if p4 priced out p3!
					p4_boundary_lo = intersection_1_4 
					p4_boundary_hi = 1 
			else:
				p4_boundary_lo = intersection_2_4 
				p4_boundary_hi = 1
		elif ((intersection_1_4 > intersection_2_4) & (intersection_1_4 > intersection_3_4)):
				p4_boundary_lo = intersection_1_4 
				p4_boundary_hi = 1 
		elif (intersection_2_4 > intersection_3_4):
				p4_boundary_lo = intersection_2_4 
				p4_boundary_hi = 1 
		else:
			p4_boundary_lo = intersection_3_4 
			p4_boundary_hi = 1 


		# //p2
		intersection_1_2 = (t *p2_l+p2_p + t * p1_l - p1_p) / (2*t)
		intersection_2_3 = (t *p3_l+p3_p + t * p2_l - p2_p) / (2*t)
		intersection_2_4 = (t *p4_l+p4_p + t * p2_l - p2_p) / (2*t)

		if ((intersection_1_2 > p2_l) | (intersection_2_3 < p2_l) | (intersection_2_4 < p2_l)):
			p2_boundary_lo = 0 
			p2_boundary_hi = 0 
		else:
			# //p2 left side
			if (intersection_1_2 >= p1_l):
				p2_boundary_lo = intersection_1_2
			elif (intersection_1_2 < p1_l):
				p2_boundary_lo = 0

			# p2 right side
			if (intersection_2_3 > p3_l):
				if (intersection_2_4 > p4_l):
					p2_boundary_hi = 1
				else:
					p2_boundary_hi = intersection_2_4
			elif (intersection_2_4 < intersection_2_3):
				p2_boundary_hi = intersection_2_4
			else:
				p2_boundary_hi = intersection_2_3


		# //p3
		intersection_1_3 = (t *p3_l+p3_p + t * p1_l - p1_p) / (2*t)
		intersection_2_3 = (t *p3_l+p3_p + t * p2_l - p2_p) / (2*t)
		intersection_3_4 = (t *p4_l+p4_p + t * p3_l - p3_p) / (2*t)

		if ((intersection_1_3 > p3_l) | (intersection_2_3 > p3_l) | (intersection_3_4 < p3_l)):
			p3_boundary_lo = 0 
			p3_boundary_hi = 0 
		else:
			# //p3 left side
			if (intersection_2_3 < p2_l):
				if (intersection_1_3 < p1_l):
					p3_boundary_lo = 0
				else:
					p3_boundary_lo = intersection_1_3
			elif (intersection_1_3 > intersection_2_3):
				p3_boundary_lo = intersection_1_3
			else:
				p3_boundary_lo = intersection_2_3

			# // p3 right side
			if (intersection_3_4 <= p4_l):
				p3_boundary_hi = intersection_3_4
			elif (intersection_3_4 > p4_l):
				p3_boundary_hi = 1


		for p in self.get_players():

			# variable setup
			if p.id_in_group == 1:
				p.boundary_lo = p1_boundary_lo
				p.boundary_hi = p1_boundary_hi
			elif p.id_in_group == 2:
				p.boundary_lo = p2_boundary_lo
				p.boundary_hi = p2_boundary_hi
			elif p.id_in_group == 3:
				p.boundary_lo = p3_boundary_lo
				p.boundary_hi = p3_boundary_hi
			elif p.id_in_group == 4:
				p.boundary_lo = p4_boundary_lo
				p.boundary_hi = p4_boundary_hi
				
			p.market_share = p.boundary_hi - p.boundary_lo
			p.round_payoff = p.market_share * p.price
			p.period_num = p.round_number
			p.cumulative_round_payoff = sum([ply.round_payoff / Constants.num_rounds for ply in p.in_all_rounds() if (ply.round_payoff != None)])



class Player(BasePlayer):

	period_number = models.PositiveIntegerField(
		doc='''period number, should match number at end of app name'''
	)

	subperiod_time = models.PositiveIntegerField(
		doc="""The length of the real effort task timer."""
	)

	transport_cost = models.FloatField(
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

	market_share = models.FloatField(
		doc='''size of player's market''')

	round_payoff = models.FloatField(
		doc="player's payoffs this round/subperiod")

	cumulative_round_payoff = models.FloatField(
		doc="player's payoffs sumulative this round/subperiod. Final round's cumulative_round_payoff is score for this period")

	paid_period = models.BooleanField(
		doc='''1/True if this is a paid period, 0/False otherwise''')



