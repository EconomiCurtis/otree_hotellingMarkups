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

"""

class Constants(BaseConstants):
    name_in_url = 'task'
    task_timer = 600 #see Subsession, before_session_starts setting. 
    num_rounds = 15
    players_per_group = 2 
    transport_cost = 1

class Subsession(BaseSubsession):

	def before_session_starts(self):

		# how long is the real effort task time? 
		# refer to settings.py settings. 
		for p in self.get_players():
			if 'subperiod_time' in self.session.config:
			    p.subperiod_time = self.session.config['subperiod_time']
			else:
			    p.subperiod_time = Constants.task_timer

			if 'transport_cost' in self.session.config:
			    p.transport_cost = self.session.config['transport_cost']
			else:
			    p.transport_cost = Constants.transport_cost

			if self.round_number == 1:
				p.price = random.uniform(0, 1)

				#set loc based on player id
				if p.id_in_group == 1: 
					p.participant.vars["loc"] = 0.25
				else: p.participant.vars["loc"] = 0.75






class Group(BaseGroup):
	pass


class Player(BasePlayer):

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

