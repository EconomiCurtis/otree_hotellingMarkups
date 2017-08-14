import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# don't share this with anybody.
SECRET_KEY = '7o$d&3y-yd2ax1vi1!)!ur8^r92y)@q^n)!7t(kih(@qbl33+5'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree'   ]

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<p>
    <a href="http://www.otree.org/" target="_blank">oTree homepage</a>.
</p>
<p>
    Here are various games implemented with oTree.
</p>
<p>
    <strong>...</strong>
</p>

"""

ROOMS = [
    {
        'name': 'leeps',
        'display_name': 'LEEPS Lab 1-12',
        'participant_label_file': '_rooms/leeps.txt',
    },
    # {
    #     'name': 'econ101',
    #     'display_name': 'Econ 101 class',
    #     'participant_label_file': '_rooms/econ101.txt',
    # },

    # {
    #     'name': 'live_demo',
    #     'display_name': 'Room for live demo (no participant labels)',
    # },
]

    
# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': '"Motherhood Experiments - RET, Compt, charity, survey"',
    'description': '...',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 10.00,
    'num_bots': 6,
    'doc': "NYUAD SSEL",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'hotellingmarkup',
        'display_name': "Hotelling Markups Tester",
        'app_sequence': [
            'hotellingmarketup_00',
            'hotellingmarkup'
        ],
        'num_demo_participants':4, # number of participants per group set in  models

        'loc':None, # set with array [], if None, then spaced (1/N)/2 apart

        #Number of Periods defined by number of arrays in t, mc and rp below. 

        'numSubperiods' :20, # number of subperiods in a period. 
        # if large, ensure 'num_rounds' in models is sufficently large
        'subperiod_time': 300, # length, in seconds, of a subperiod

        # below, each array indicate subperiod values for t, mc, and rp (and whatever else)
        # if there are too few elements in a period's array, the array is repeated until numSubperiods. 
        't':[
            [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,],
            [0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,],
            [0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,],
            [0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50 ],
            [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,],
            [0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,0.1 ,],
            [0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,],
            [0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50 ],
            [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,],
            [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,],
        ], #shopping cost, each element is one subperiod in a period. 
        'mc':[
            [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,],
            [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,],
            [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,],
            [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,],
            [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,],
            [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,],
            [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,],
            [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,],
            [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,],
            [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,],

        ], #firm mill cost, or per item cost, each element is one subperiod in a period. 
        'rp':[
            [1.00,],
            [0.95,],
            [1.00,],
            [0.95],
            [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,],
            [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,],
            [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,],
            [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,],
            [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,],
            [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,],
        ], # consumer reserve price,  each element is one subperiod in a period. 

    },

    {
        'name': 'hotellingmarkup_01_4p_sess01',
        'display_name': "Hotelling Markups - 4 player - T=0.75, 0.25,   0.5,    1,  0.1,    0.25,   0.5,    1,  0.1,    0.75,   1,  0.1,    0.75,   0.25,   0.5   - 20 7-sec subperiods",
        'num_demo_participants': 4,
        'app_sequence': [
            'hotellingmarketup_00',
            'hotellingmarkup_4p_075t_01',
            'hotellingmarkup_4p_025t_02',
            'hotellingmarkup_4p_050t_03',
            'hotellingmarkup_4p_100t_04',
            'hotellingmarkup_4p_010t_05',
            'hotellingmarkup_4p_025t_06',
            'hotellingmarkup_4p_050t_07',
            'hotellingmarkup_4p_100t_08',
            'hotellingmarkup_4p_010t_09',
            'hotellingmarkup_4p_075t_10',
            'hotellingmarkup_4p_100t_11',
            'hotellingmarkup_4p_010t_12',
            'hotellingmarkup_4p_075t_13',
            'hotellingmarkup_4p_025t_14',
            'hotellingmarkup_4p_050t_15',
            'hotellingmarkup_payment_20'
        ],
        'subperiod_time': 7,
        'p1_loc':0.125,
        'p2_loc':0.375,
        'p3_loc':0.625,
        'p4_loc':0.875, 
    },
    {
        'name': 'hotellingmarkup_01_2p_sess02',
        'display_name': "Hotelling Markups - 2 player - T=0.75, 0.25,   0.5,    1,  0.1,    0.25,   0.5,    1,  0.1,    0.75,   1,  0.1,    0.75,   0.25,   0.5  - 20 7-sec subperiods",
        'num_demo_participants': 2,
        'app_sequence': [
            'hotellingmarketup_00',
            'hotellingmarkup_2p_075t_01',
            'hotellingmarkup_2p_025t_02',
            'hotellingmarkup_2p_050t_03',
            'hotellingmarkup_2p_100t_04',
            'hotellingmarkup_2p_010t_05',
            'hotellingmarkup_2p_025t_06',
            'hotellingmarkup_2p_050t_07',
            'hotellingmarkup_2p_100t_08',
            'hotellingmarkup_2p_010t_09',
            'hotellingmarkup_2p_075t_10',
            'hotellingmarkup_2p_100t_11',
            'hotellingmarkup_2p_010t_12',
            'hotellingmarkup_2p_075t_13',
            'hotellingmarkup_2p_025t_14',
            'hotellingmarkup_2p_050t_15',
            'hotellingmarkup_payment_20'
        ],
        'subperiod_time': 7,
        # 'p1_loc':0.125,
        # 'p2_loc':0.375,
        # 'p3_loc':0.625,
        # 'p4_loc':0.875, 
    },

    {
        'name': 'hotellingmarkup_01_2p_test',
        'display_name': "Hotelling Markups - 2 player - 1-periods of each; T=0.1,0.25,0.5,0.75,1.0 - 20 7-sec subperiods",
        'num_demo_participants': 2,
        'app_sequence': [
            'hotellingmarketup_00',
            'hotellingmarkup_2p_010t_01',
            'hotellingmarkup_2p_025t_01',
            'hotellingmarkup_2p_050t_01',
            'hotellingmarkup_2p_075t_01',
            'hotellingmarkup_2p_100t_01',
            'hotellingmarkup_payment_20'
        ],
        'subperiod_time': 5,
    },
    # {
    #     'name': 'hotellingmarkup_01_4p_050t',
    #     'display_name': "Hotelling Markups - 4 player - t=0.5",
    #     'num_demo_participants': 4,
    #     'app_sequence': [
    #         'hotellingmarketup_00',
    #         'hotellingmarkup_4p_050t_01',
    #         'hotellingmarkup_payment_20'
    #     ],
    #     'subperiod_time': 7,
    #     'p1_loc':0.125,
    #     'p2_loc':0.375,
    #     'p3_loc':0.625,
    #     'p4_loc':0.875,
    # },
    # {
    #     'name': 'hotellingmarkup_01_4p_010t',
    #     'display_name': "Hotelling Markups - 4 player - t=0.1",
    #     'num_demo_participants': 4,
    #     'app_sequence': [
    #         'hotellingmarketup_00',
    #         'hotellingmarkup_4p_010t_01',
    #         'hotellingmarkup_payment_20'
    #     ],
    #     'subperiod_time': 7,
    #     'p1_loc':0.125,
    #     'p2_loc':0.375,
    #     'p3_loc':0.625,
    #     'p4_loc':0.875,
    # },


    # {
    #     'name': 'public_goods',
    #     'display_name': "oTree Demo - Public Goods",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['public_goods', 'payment_info'],
    # },
    # {
    #     'name': 'trust',
    #     'display_name': "oTree Demo - Trust Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['trust', 'payment_info'],
    # },
    # {
    #     'name': 'beauty',
    #     'display_name': "oTree Demo - Beauty Contest",
    #     'num_demo_participants': 5,
    #     'num_bots': 5,
    #     'app_sequence': ['beauty', 'payment_info'],
    # },
    # {
    #     'name': 'survey',
    #     'display_name': "oTree Demo - Survey",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['survey', 'payment_info'],
    # },
    # {
    #     'name': 'prisoner',
    #     'display_name': "oTree Demo - Prisoner's Dilemma",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['prisoner', 'payment_info'],
    # },
    # {
    #     'name': 'ultimatum',
    #     'display_name': "oTree Demo - Ultimatum (randomized: strategy vs. direct response)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    # },
    # {
    #     'name': 'ultimatum_strategy',
    #     'display_name': "oTree Demo - Ultimatum (strategy method treatment)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    #     'treatment': 'strategy',
    # },
    # {
    #     'name': 'ultimatum_non_strategy',
    #     'display_name': "oTree Demo - Ultimatum (direct response treatment)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    #     'treatment': 'direct_response',
    # },
    # {
    #     'name': 'battle_of_the_sexes',
    #     'display_name': "oTree Demo - Battle of the Sexes",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'battle_of_the_sexes', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'vickrey_auction',
    #     'display_name': "oTree Demo - Vickrey Auction",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['vickrey_auction', 'payment_info'],
    # },
    # {
    #     'name': 'volunteer_dilemma',
    #     'display_name': "oTree Demo - Volunteer's Dilemma",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['volunteer_dilemma', 'payment_info'],
    # },
    # {
    #     'name': 'cournot',
    #     'display_name': "oTree Demo - Cournot Competition",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'cournot', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'principal_agent',
    #     'display_name': "oTree Demo - Principal Agent",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['principal_agent', 'payment_info'],
    # },
    # {
    #     'name': 'dictator',
    #     'display_name': "oTree Demo - Dictator Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['dictator', 'payment_info'],
    # },
    # {
    #     'name': 'matching_pennies',
    #     'display_name': "oTree Demo - Matching Pennies",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'matching_pennies',
    #     ],
    # },
    # {
    #     'name': 'traveler_dilemma',
    #     'display_name': "oTree Demo - Traveler's Dilemma",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['traveler_dilemma', 'payment_info'],
    # },
    # {
    #     'name': 'bargaining',
    #     'display_name': "oTree Demo - Bargaining Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['bargaining', 'payment_info'],
    # },
    # {
    #     'name': 'common_value_auction',
    #     'display_name': "oTree Demo - Common Value Auction",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['common_value_auction', 'payment_info'],
    # },
    # {
    #     'name': 'stackelberg',
    #     'display_name': "oTree Demo - Stackelberg Competition",
    #     'real_world_currency_per_point': 0.01,
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'stackelberg', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'bertrand',
    #     'display_name': "oTree Demo - Bertrand Competition",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'bertrand', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'stag_hunt',
    #     'display_name': "oTree Demo - Stag Hunt",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['stag_hunt', 'payment_info'],
    # },
    # {
    #     'name': 'real_effort',
    #     'display_name': "oTree Demo - Real-effort transcription task",
    #     'num_demo_participants': 1,
    #     'app_sequence': [
    #         'real_effort',
    #     ],
    # },
    # {
    #     'name': 'lemon_market',
    #     'display_name': "oTree Demo - Lemon Market Game",
    #     'num_demo_participants': 3,
    #     'app_sequence': [
    #         'lemon_market', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'public_goods_simple',
    #     'display_name': "oTree Demo - Public Goods (simple version from tutorial)",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    # },

    # {
    #     'name': 'trust_simple',
    #     'display_name': "oTree Demo - Trust Game (simple version from tutorial)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['trust_simple'],
    # },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
