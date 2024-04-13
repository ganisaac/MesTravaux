import pandas as pd
from dash import Dash, Input, Output, dcc, html, no_update
import dash_bootstrap_components as dbc
from datetime import date
from business.objects.option import Option
from business.services.opt_service import OptionsService
from business.services.bs_formula import BS_formula
from business.services.bs_formula_straddle import BS_formula_Straddle
from business.services.asian_mc_pricer import AsianMCPricer
from business.objects.person import Person
from business.objects.swap import Swap
from business.services.swappricer import SwapPricer

from dateutil.relativedelta import relativedelta
from dash.exceptions import PreventUpdate

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objs as go
from plotly.validator_cache import ValidatorCache



def get_relative_maturity(maturity):
    
    maturity = pd.to_datetime(maturity, format="%Y-%m-%d")

    initial_date = date(2023, 12, 8)

    temp_maturity = date(maturity.year, maturity.month, maturity.day)
    rel_maturity = relativedelta(temp_maturity, initial_date)
    rel_maturity = (
        rel_maturity.years + rel_maturity.months / 12.0 + rel_maturity.days / 365.25
    )
    
    return rel_maturity

options = ["Apple", "Amazon", "Ali Baba", "Google", "Meta", "Microsoft", "Sony", "Tesla"]
types=["Put","Call"]
grecques=["Delta","Gamma","Vega","Theta","Rho"]
directions = ["Pay", "Receive"]
discountindexs = ['SOFR', 'BGCR', 'TGCR']

header = html.Div(
                dbc.Row(
                [
                    dbc.Col(html.Div(children = [
                        dcc.Link("Pricing d'options Européennes", href="/page1", className="button")]),
                        width={"size":3}
                        ),
                    dbc.Col(html.Div(children = [
                        dcc.Link("Pricing de straddle", href="/page2", className="button")]),
                        width={"size":3}
                        ),
                    dbc.Col(html.Div(children = [
                        dcc.Link("Pricing de swaps de taux", href="/page3", className="button")]),
                        width={"size":3}
                        ),
                    dbc.Col(html.Div(children = [
                        dcc.Link("Pricing d'options Asiatiques", href="/page4", className="button")]),
                        width={"size":3}
                        )
                        ])
)

card_volatility = [
    dbc.CardHeader( 
                   html.H3("Volatilité implicite", className="card-title"),
),
    dbc.CardBody(
        [
            html.Div(
                id="id_volatility",
                className="card-text",
            ),
            
        ]
    ),
]

card_volatilities = [
    dbc.CardHeader(html.H3("Volatilités implicites", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Call"]), html.Td(id='id_volatility_call')]),
        html.Tr([html.Td(["Put"]), html.Td(id='id_volatility_put')]),
    ]),)]

card_price = [
    dbc.CardHeader(html.H3("Prix de l'option", className="card-title"),),
    dbc.CardBody(
        [
            html.Div(
                id="id_price",
                className="card-text",
            ),
            
        ]
    ),
]


card_figure_greek = [
    dbc.CardHeader(html.H3("Graphique des grecques en fonction du prix du sous-jacent", className="card-title"),),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Grecque", className="menu-title"),
                        dcc.Dropdown(
                            id="grecque-filter",
                            options=[
                                {"label": grecque, "value": grecque} for grecque in grecques
                            ],
                            value="Delta",
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                )),
                dbc.Col(
                     html.Div(
                    children=[
                        html.Div(children="Min", className="menu-title"),
                        dcc.Input(
                            id="min_S-filter",
                            type="number",
                            value=50,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),
                ),
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Max", className="menu-title"),
                        dcc.Input(
                            id="max_S-filter",
                            type="number",
                            value=500,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),)
                ]),
         
            dcc.Graph(
                        id='greek-graph',
                        figure={}
                    )
            
        ]
    ),
]

card_figure_strike =  [
    dbc.CardHeader(html.H3("Graphique des grecques en fonction du strike", className="card-title"),),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Grecque", className="menu-title"),
                        dcc.Dropdown(
                            id="strike_final-filter",
                            options=[
                                {"label": grecque, "value": grecque} for grecque in grecques
                            ],
                            value="Delta",
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                )),
                dbc.Col(
                     html.Div(
                    children=[
                        html.Div(children="Min", className="menu-title"),
                        dcc.Input(
                            id="min_K-filter",
                            type="number",
                            value=50,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),
                ),
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Max", className="menu-title"),
                        dcc.Input(
                            id="max_K-filter",
                            type="number",
                            value=500,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),)
                ]),
         
            dcc.Graph(
                        id='strike_final-graph',
                        figure={}
                    )
            
        ]
    ),
]

card_price_str = [
    dbc.CardHeader(html.H3("Prix du straddle", className="card-title"),),
    dbc.CardBody(
        [
            html.Div(
                id="id_price_str",
                className="card-text",
            ),
            
        ]
    ),
]

card_table = [
    dbc.CardHeader(html.H3("Grecques de l'option", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Delta"]), html.Td(id='delta')]),
        html.Tr([html.Td(["Gamma"]), html.Td(id='gamma')]),
        html.Tr([html.Td(["Vega"]), html.Td(id='vega')]),
        html.Tr([html.Td(["Theta"]), html.Td(id='theta')]),
        html.Tr([html.Td(["Rho"]), html.Td(id='rho')]),
    ]),)
    
    ]

card_table_str = [
    dbc.CardHeader(html.H3("Grecques du straddle", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Delta"]), html.Td(id='delta_str')]),
        html.Tr([html.Td(["Gamma"]), html.Td(id='gamma_str')]),
        html.Tr([html.Td(["Vega"]), html.Td(id='vega_str')]),
        html.Tr([html.Td(["Theta"]), html.Td(id='theta_str')]),
        html.Tr([html.Td(["Rho"]), html.Td(id='rho_str')]),
    ]),)
    
    ]

card_figure_greek_str = [
    dbc.CardHeader(html.H3("Graphique des grecques en fonction du prix du sous-jacent", className="card-title"),),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Grecque", className="menu-title"),
                        dcc.Dropdown(
                            id="grecque-filter-str",
                            options=[
                                {"label": grecque, "value": grecque} for grecque in grecques
                            ],
                            value="Delta",
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                )),
                dbc.Col(
                     html.Div(
                    children=[
                        html.Div(children="Min", className="menu-title"),
                        dcc.Input(
                            id="min_S-filter-str",
                            type="number",
                            value=50,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),
                ),
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Max", className="menu-title"),
                        dcc.Input(
                            id="max_S-filter-str",
                            type="number",
                            value=500,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),)
                ]),
         
            dcc.Graph(
                        id='greek-graph-str',
                        figure={}
                    )
            
        ]
    ),
]

card_figure_strikec =  [
    dbc.CardHeader(html.H3("Graphique des grecques en fonction du strike Call", className="card-title"),),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Grecque", className="menu-title"),
                        dcc.Dropdown(
                            id="strikec_final-filter-str",
                            options=[
                                {"label": grecque, "value": grecque} for grecque in grecques
                            ],
                            value="Delta",
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                )),
                dbc.Col(
                     html.Div(
                    children=[
                        html.Div(children="Min", className="menu-title"),
                        dcc.Input(
                            id="min_Kc-filter-str",
                            type="number",
                            value=50,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),
                ),
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Max", className="menu-title"),
                        dcc.Input(
                            id="max_Kc-filter-str",
                            type="number",
                            value=500,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),)
                ]),
         
            dcc.Graph(
                        id='strikec_final-graph_str',
                        figure={}
                    )
            
        ]
    ),
]

card_figure_strikep =  [
    dbc.CardHeader(html.H3("Graphique des grecques en fonction du strike Put", className="card-title"),),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Grecque", className="menu-title"),
                        dcc.Dropdown(
                            id="strikep_final-filter-str",
                            options=[
                                {"label": grecque, "value": grecque} for grecque in grecques
                            ],
                            value="Delta",
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                )),
                dbc.Col(
                     html.Div(
                    children=[
                        html.Div(children="Min", className="menu-title"),
                        dcc.Input(
                            id="min_Kp-filter-str",
                            type="number",
                            value=50,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),
                ),
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Max", className="menu-title"),
                        dcc.Input(
                            id="max_Kp-filter-str",
                            type="number",
                            value=500,
                            style={"height": 40, "width":110, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],
                ),)
                ]),
         
            dcc.Graph(
                        id='strikep_final-graph_str',
                        figure={}
                    )
            
        ]
    ),
]

card_table_sw = [
    dbc.CardHeader(html.H3("Taux obligataires", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Maturité T1 jambe fixe"]), html.Td(id='discount_t1_fix')]),
        html.Tr([html.Td(["Maturité Tn jambe fixe"]), html.Td(id='discount_tn_fix')]),
        html.Tr([html.Td(["Maturité T1 jambe variable"]), html.Td(id='discount_t1_var')]),
        html.Tr([html.Td(["Maturité Tn jambe variable"]), html.Td(id='discount_tn_var')]),
    ]),)
    
    ]

card_leg_table = [
    dbc.CardHeader(html.H3("Valeur de jambe", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Jambe fixe"]), html.Td(id='pv_fix')]),
        html.Tr([html.Td(["Jambe variable"]), html.Td(id='pv_float')]),
    ]),)
    
    ]


card_price_sw = [
    dbc.CardHeader(html.H3("Prix du swap", className="card-title"),),
    dbc.CardBody(
        [
            html.Div(
                id="id_price_sw",
                className="card-text",
            ),
            
        ]
    ),
]

card_hist_volatility = [
    dbc.CardHeader( 
                   html.H3("Volatilité historique", className="card-title"),
),
    dbc.CardBody(
        [
            html.Div(
                id="hist_volatility",
                className="card-text",
            ),
            
        ]
    ),
]

card_asian_price = [
    dbc.CardHeader(html.H3("Prix de l'option", className="card-title"),),
    dbc.CardBody(
        [
            html.Div(
                id="id_asian_price",
                className="card-text",
            ),
            
        ]
    ),
]

card_asian_table = [
    dbc.CardHeader(html.H3("Grecques de l'option", className="card-title"),),
    dbc.CardBody(
    html.Table([
        html.Tr([html.Td(["Delta"]), html.Td(id='asian_delta')]),
        html.Tr([html.Td(["Gamma"]), html.Td(id='asian_gamma')]),
        html.Tr([html.Td(["Vega"]), html.Td(id='asian_vega')]),
    ]),)
    
    ]


app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR], suppress_callback_exceptions=True)

server = app.server

content = html.Div(id="page-content", style={"margin-top": "60px", "padding": "20px"})

app.layout = html.Div([dcc.Location(id="url"), header, content])

def page1_layout():
    return dbc.Container(
    [   
        html.Div(
                children=[
                    html.P(children="🪙", className="header-emoji"),
                    html.H1(children="Pricing d'options Européennes", className="header-title"),
                    html.P(
                        children=(
                            "Dans cette page, nous mettons à disposition un outil de pricing d'options Européennes selon le modèle de Black-Scholes."
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        html.Div(
            [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Sous-jacent", className="menu-title"),
                        dcc.Dropdown(
                            id="option-filter",
                            options=[
                                {"label": option, "value": option} for option in options
                            ],
                            value="Apple",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                ),
                    width={"size":3,"offset":2}),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": type,
                                    "value": type,
                                }
                                for type in types
                            ],
                            value="Call",
                            style={"height": 40, "width":150,  "border-radius": "1em", "border": "3px solid #ccc"},
                            clearable=False,
                            searchable=False,
                            
                        ),
                    ],
                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Maturité", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="date",
                            min_date_allowed=date(2023,12,10),
                            max_date_allowed=date(2030,12,31),
                            initial_visible_month=date(2023,12,10),
                            date=date(2024,12,8),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),
                
            ]
            ),
        dbc.Row(
            [
                dbc.Col(                
                    html.Div(
                    children=[
                        html.Div(children="S0", className="menu-title"),
                        dcc.Input(
                            id="s0-filter",
                            type="number",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],

                ),
                    width={"size":3,"offset":2}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Strike", className="menu-title"),
                        dcc.Input(
                            id="strike-filter",
                            type="number",
                            value=100,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Taux d'intérêt", className="menu-title"),
                        dcc.Input(
                            id="rate-filter",
                            type="number",
                            value=0.052,
                            style={"height": 40, "width":130, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
            ],
        ),
            ],
            className="menu",
),
            
            dbc.Row(
                [
                    #two graphs here in two columns
                    dbc.Col([dbc.Card(card_volatility, color="white", inverse=False,outline=False)
                        ,dbc.Card(card_price, color="white", inverse=False,outline=False)]
                            ,width={"size":5,"offset":1}),

                    
                    dbc.Col(dbc.Card(
                        card_table
                        , color="white", inverse=False,outline=False),
                            ),
                ]
                ,justify="around",
                style={"margin-top": 10},),

            dbc.Row(
            [
                #two graphs here in two columns
                dbc.Col([dbc.Card(card_figure_greek, color="white", inverse=False,outline=False)
                    ]
                        ,width={"size":5,"offset":1}),

                
                dbc.Col(dbc.Card(
                    card_figure_strike
                    , color="white", inverse=False,outline=False),
                        ),
            ]
            ,justify="around",
            style={"margin-top": 10},),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Volatilité implicite", className="menu-title"),
                        dcc.Graph(
                        id='volatility_implicite-graph',
                        figure={}
                    ),
                    ]
                ),
                    width={"size":12}
                    ),
            ]),
        
    ],fluid=True    
)

def page2_layout():
    return dbc.Container(
    [ 
        html.Div(
                children=[
                    html.P(children="🪙", className="header-emoji"),
                    html.H1(children="Pricing de straddle", className="header-title"),
                    html.P(
                        children=(
                            "Dans cette page, nous mettons à disposition un outil de pricing d'un Straddle selon le modèle de Black-Scholes."
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        html.Div(
            [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Sous-jacent", className="menu-title"),
                        dcc.Dropdown(
                            id="option-filter-str",
                            options=[
                                {"label": option, "value": option} for option in options
                            ],
                            value="Apple",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                ),
                    width={"size":3,"offset":2}),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Strike call", className="menu-title"),
                        dcc.Input(
                            id="strike-call-filter",
                            type="number",
                            value=150,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Maturité", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="date-str",
                            min_date_allowed=date(2023,12,10),
                            max_date_allowed=date(2030,12,31),
                            initial_visible_month=date(2023,12,10),
                            date=date(2024,12,8),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),
                
            ]
            ),
        dbc.Row(
            [
                dbc.Col(                
                    html.Div(
                    children=[
                        html.Div(children="S0", className="menu-title"),
                        dcc.Input(
                            id="s0-filter-str",
                            type="number",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],

                ),
                    width={"size":3,"offset":2}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Strike put", className="menu-title"),
                        dcc.Input(
                            id="strike-put-filter",
                            type="number",
                            value=100,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Taux d'intérêt", className="menu-title"),
                        dcc.Input(
                            id="rate-filter-str",
                            type="number",
                            value=0.052,
                            style={"height": 40, "width":130, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
            ],
        ),
            ],
            className="menu",
),
            
            dbc.Row(
                [
                    #two graphs here in two columns
                    dbc.Col([dbc.Card(card_volatilities, color="white", inverse=False,outline=False),
                        dbc.Card(card_price_str, color="white", inverse=False,outline=False)]
                            ,width={"size":5,"offset":1}),

                    
                    dbc.Col(dbc.Card(
                        card_table_str
                        , color="white", inverse=False,outline=False),
                            ),
                ]
                ,justify="around",
                style={"margin-top": 10},),
            dbc.Row(
            [
                #two graphs here in two columns
                dbc.Col([dbc.Card(card_figure_greek_str, color="white", inverse=False,outline=False)
                    ]
                        ,width={"size":4}),

                
                dbc.Col(dbc.Card(
                    card_figure_strikec
                    , color="white", inverse=False,outline=False),
                        width={"size":4}),
                dbc.Col(dbc.Card(
                    card_figure_strikep
                    , color="white", inverse=False,outline=False),
                        width={"size":4}),
            ]
            ,justify="around",
            style={"margin-top": 10},),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children=[
                        html.Div(children="Volatilité implicite", className="menu-title"),
                        dcc.Graph(
                        id='volatility_implicite-graph-str',
                        figure={}
                    ),
                    ]
                ),
                    width={"size":12}
                    ),
            ]),
    ],fluid=True    
)

def page3_layout():


    return dbc.Container(
    [ 
        html.Div(
                children=[
                    html.P(children="🪙", className="header-emoji"),
                    html.H1(children="Pricing de swaps de taux", className="header-title"),
                    html.P(
                        children=(
                            "Dans cette page, nous mettons à disposition un outil de pricing d'un Swap de taux."
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        html.Div(
            [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Direction", className="menu-title"),
                        dcc.Dropdown(
                            id="direction",
                            options=[
                                {"label": direction, "value": direction} for direction in directions
                            ],
                            value="Pay",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                ),
                    width={"size":3, 'offset':2}),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Notionnel", className="menu-title"),
                        dcc.Input(
                            id="notionnel",
                            type="number",
                            value=10000,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Date de pricing", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="date-pr-sw",
                            min_date_allowed=date(2023,1,1),
                            max_date_allowed=date(2030,12,31),
                            initial_visible_month=date.today(),
                            date=date.today(),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),            
            ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Index taux ", className="menu-title"),
                        dcc.Dropdown(
                            id="discountindex",
                            options=[
                                {"label": index, "value": index} for index in discountindexs
                            ],
                            value="SOFR",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                ),
                    width={"size":3,"offset":2}),

                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Date de valeur", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="val-date-sw",
                            min_date_allowed=date(2024,1,1),
                            max_date_allowed=date(2040,12,31),
                            initial_visible_month=date(2024,6,1),
                            date=date(2024,6,1),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),

                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Maturité", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="date-sw",
                            min_date_allowed=date(2023,12,10),
                            max_date_allowed=date(2060,12,31),
                            initial_visible_month=date(2025,1,1),
                            date=date(2025,1,1),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(                
                    html.Div(
                    children=[
                        html.Div(children="Fréquence de la jambe fixe (mois)", className="menu-title"),
                        dcc.Input(
                            id="fixed_frequency",
                            type="number",
                            value=12,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3,"offset":2}
                    ),
                dbc.Col(                
                    html.Div(
                    children=[
                        html.Div(children="Fréquence de la jambe variable (mois)", className="menu-title"),
                        dcc.Input(
                            id="float_frequency",
                            type="number",
                            value=12,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Taux fixe", className="menu-title"),
                        dcc.Input(
                            id="fixed_rate_sw_1",
                            type="number",
                            value=0.052,
                            style={"height": 50, "width":150, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
            ],
        ),
            ],
            className="menu",
),
            
            dbc.Row(
                [
                    
                    dbc.Col(dbc.Card(
                        card_table_sw
                        , color="white", inverse=False,outline=False),
                        width={"size":5,"offset":0},
                            ),
                    dbc.Col([dbc.Card(card_price_sw, color="white", inverse=False,outline=False),
                             dbc.Card(card_leg_table,color="white", inverse=False,outline=False )]
                            ,width={"size":5,"offset":0}),
                ]
                ,justify="around",
                style={"margin-top": 10},),
    ],fluid=True    
)

def page4_layout():
    return dbc.Container(
    [   
        html.Div(
                children=[
                    html.P(children="🪙", className="header-emoji"),
                    html.H1(children="Pricing d'options Asiatiques", className="header-title"),
                    html.P(
                        children=(
                            "Sur cette page, nous mettons en place un outil de pricing d'une option Asiatique par Monte Carlo en suivant l'équation de Black-Scholes."
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        html.Div(
            [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Sous-jacent", className="menu-title"),
                        dcc.Dropdown(
                            id="option-asian-filter",
                            options=[
                                {"label": option, "value": option} for option in options
                            ],
                            value="Apple",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},                            
                            clearable=False,
                        ),
                    ]
                ),
                    width={"size":3,"offset":1}),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-asian-filter",
                            options=[
                                {
                                    "label": type,
                                    "value": type,
                                }
                                for type in types
                            ],
                            value="Call",
                            style={"height": 40, "width":150,  "border-radius": "1em", "border": "3px solid #ccc"},
                            clearable=False,
                            searchable=False,
                            
                        ),
                    ],
                ),
                    width={"size":3}
                    ),

                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Maturité", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="asian_date",
                            min_date_allowed=date(2023,12,10),
                            max_date_allowed=date(2030,12,31),
                            initial_visible_month=date(2023,12,10),
                            date=date(2024,12,8),
                            style={ "border-radius": "1em", "border": "3px solid #ccc"}
                        ),
                    ]
                ),
                    width={"size":3}
                    ),
                
            ]
            ),
        dbc.Row(
            [
                dbc.Col(                
                    html.Div(
                    children=[
                        html.Div(children="S0", className="menu-title"),
                        dcc.Input(
                            id="s0-asian-filter",
                            type="number",
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                        ),
                    ],

                ),
                    width={"size":3,"offset":1}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Strike", className="menu-title"),
                        dcc.Input(
                            id="strike-asian-filter",
                            type="number",
                            value=100,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Taux d'intérêt", className="menu-title"),
                        dcc.Input(
                            id="rate-asian-filter",
                            type="number",
                            value=0.052,
                            style={"height": 40, "width":130, "border-radius": "1em", "border": "3px solid #ccc", "margin-bottom": 10},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Simulations", className="menu-title"),
                        dcc.Input(
                            id="n_simul-filter",
                            type="number",
                            value=1000,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3, "offset":1}
                    ),
                dbc.Col(
                    html.Div(
                    children=[
                        html.Div(children="Fenêtre", className="menu-title"),
                        dcc.Input(
                            id="fen-filter",
                            type="number",
                            value=20,
                            style={"height": 40, "width":150, "border-radius": "1em", "border": "3px solid #ccc"},
                            className="dropdown",
                        ),
                    ],

                ),
                    width={"size":3}
                    ),
            ],
        ),
        ],
            className="menu",
),

            
            dbc.Row(
                [
                    dbc.Col([dbc.Card(card_hist_volatility, color="white", inverse=False,outline=False)
                        ,dbc.Card(card_asian_price, color="white", inverse=False,outline=False)]
                            ,width={"size":5,"offset":1}),

                    
                    dbc.Col(dbc.Card(
                        card_asian_table
                        , color="white", inverse=False,outline=False),
                            ),
                ]
                ,justify="around",
                style={"margin-top": 10},),
    ],fluid=True 
    )


page1 = page1_layout()
page2 = page2_layout()
page3 = page3_layout()
page4 = page4_layout()


@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname"))

def display_page(pathname):
    if pathname is None or pathname == "/":
        pathname = "/page1"
    global path
    path = pathname
    if pathname == "/page1":
        return page1
    elif pathname == "/page2":
        return page2
    elif pathname == "/page3":
        return page3
    elif pathname == "/page4":
        return page4
    else:
        return html.H1("404 - Page not found")


@app.callback(
    Output("s0-filter", "value"),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
)
def update_s0(option, types):
    if path != "/page1":
        return no_update
    else:
        O=Option(option,K=None,T=None)
        return  O.S0

#callback for the volatility take the option and the type and return the volatility

@app.callback(
    Output("id_volatility", "children"),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
    Input("date", "date"),
    Input("s0-filter", "value"),
    Input("strike-filter", "value"),
    Input("rate-filter", "value"),
    
)
def update_volatility(option, types, date, s0, strike, rate):
    
    if path != "/page1":
        return no_update
    else:
        if s0 is None or strike is None or rate is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            P=Person(types)
            opt_service=OptionsService()

            sigma=opt_service.calcul_impl_volatility(O,P)

            
            return round(sigma[0],2)
# Callback for the price take the option , the type and the sigma and return the price and the greeks

@app.callback(
    Output("id_price", "children"),
    Output('delta', 'children'),
    Output('gamma', 'children'),
    Output('vega', 'children'),
    Output('theta', 'children'),
    Output('rho', 'children'),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
    Input("date", "date"),
    Input("s0-filter", "value"),
    Input("strike-filter", "value"),
    Input("rate-filter", "value"),
    Input("id_volatility", "children"),
)
def update_price(option, types, date, s0, strike, rate, sigma):
    if path != "/page1":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            P=Person(types)

            
            bsm = BS_formula( O, P,sigma=float(sigma))
            price = f"{bsm.BS_price():.2f} €"
            delta=f"{bsm.BS_delta():.2f}"

            gamma=f"{bsm.BS_gamma():.2f}"
            vega=f"{bsm.BS_vega():.2f}"
            theta=f"{bsm.BS_theta():.2f}"
            
            rho=f"{bsm.BS_rho():.2f}"
            
            return price, delta, gamma, vega, theta, rho


@app.callback(
    Output('greek-graph', 'figure'),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
    Input("date", "date"),
    Input("s0-filter", "value"),
    Input("strike-filter", "value"),
    Input("rate-filter", "value"),
    Input("id_volatility", "children"),
    Input("grecque-filter", "value"),
    Input("min_S-filter", "value"),
    Input("max_S-filter", "value"),
)

def update_graph(option, types, date, s0, strike, rate, sigma, grecque,min_S,max_S):
    """
    This function take the option, the type, the date, the s0, the strike and the rate and return the volatility
    Args:
        option (string): option name
        types (string): call or put
        date (string): date of maturity
        s0 (string): price of the underlying asset
        strike (_type_): strike price
        rate (_type_): risk free rate
    """
    if path != "/page1":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            T = get_relative_maturity(date)
            d1 = (np.log(O.S0 / O.K) + (O.r + 0.5 * sigma**2) * O.T) / (sigma * np.sqrt(O.T))
            d2 = d1 - sigma * np.sqrt(O.T)

            # Fonction qui calcule les greeks en fonction de S
            def greek(S,grecque,types):
                d1 = (np.log(S / O.K) + (O.r + 0.5 * sigma**2) * O.T) / (sigma * np.sqrt(O.T))
                d2 = d1 - sigma * np.sqrt(O.T)
                delta_c = norm.cdf(d1)
                delta_p = norm.cdf(d1)-1
                
                    # Gamma
                gamma = norm.pdf(d1) / (S * sigma * np.sqrt(O.T))
        
                    # Vega
                vega = S * norm.pdf(d1) * np.sqrt(O.T)
        
                    # Theta
                theta_c = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(O.T)) - O.r * O.K * np.exp(-O.r * O.T) * norm.cdf(d2)
                theta_p = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(O.T)) + O.r * O.K * np.exp(-O.r * O.T) * norm.cdf(-d2) 
        
                    # Rho
                rho_c = O.K * O.T * np.exp(-O.r * O.T) * norm.cdf(d2)
                rho_p = -O.K * O.T * np.exp(-O.r * O.T) * norm.cdf(-d2)
                
                if grecque=="Delta":
                    if types=="Call":
                        return delta_c
                    else:
                        return delta_p
                elif grecque=="Gamma":
                    return gamma
                elif grecque=="Vega":
                    return vega
                elif grecque=="Theta":
                    if types=="Call":
                        return theta_c
                    else:
                        return theta_p
                else: 
                    if types=="Call":
                        return rho_c
                    else:
                        return rho_p
                
            S = list(range(min_S,max_S))
            greeks = [greek(i,grecque,types) for i in S]    
                
            # Change the color in red
            fig = go.Figure(data=[go.Scatter(x=S, y=greeks, line=dict(color="red", width=2))])

            return fig
@app.callback(
    Output('strike_final-graph', 'figure'),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
    Input("date", "date"),
    Input("s0-filter", "value"),
    Input("strike-filter", "value"),
    Input("rate-filter", "value"),
    Input("id_volatility", "children"),
    Input("strike_final-filter", "value"),
    Input("min_K-filter", "value"),
    Input("max_K-filter", "value"),
)
def update_strike(option, types, date, s0, strike, rate, sigma, grecque,min_K,max_K):
    if path != "/page1":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            T = get_relative_maturity(date)
            d1 = (np.log(O.S0 / O.K) + (O.r + 0.5 * sigma**2) * O.T) / (sigma * np.sqrt(O.T))
            d2 = d1 - sigma * np.sqrt(O.T)

            # Fonction qui calcule les greeks en fonction de S
            def greek(K,grecque, types):
                d1 = (np.log(O.S0 / K) + (O.r + 0.5 * sigma**2) * O.T) / (sigma * np.sqrt(O.T))
                d2 = d1 - sigma * np.sqrt(O.T)
                delta_c = norm.cdf(d1)
                delta_p = norm.cdf(d1)-1
                
        
                    # Gamma
                gamma = norm.pdf(d1) / (O.S0 * sigma * np.sqrt(O.T))
        
                    # Vega
                vega = O.S0 * norm.pdf(d1) * np.sqrt(O.T)
        
                    # Theta
                theta_c = -(O.S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(O.T)) - O.r * K * np.exp(-O.r * O.T) * norm.cdf(d2)
                theta_p = -(O.S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(O.T)) + O.r * K * np.exp(-O.r * O.T) * norm.cdf(-d2) 
        
                    # Rho
                rho_c = K * O.T * np.exp(-O.r * O.T) * norm.cdf(d2)
                rho_p = -K * O.T * np.exp(-O.r * O.T) * norm.cdf(-d2)
                
                if grecque=="Delta":
                    if types=="Call":
                        return delta_c
                    else:
                        return delta_p
                elif grecque=="Gamma":
                    return gamma
                elif grecque=="Vega":
                    return vega
                elif grecque=="Theta":
                    if types=="Call":
                        return theta_c
                    else:
                        return theta_p
                else: 
                    if types=="Call":
                        return rho_c
                    else:
                        return rho_p
                
            K = list(range(min_K,max_K))
            greeks = [greek(i,grecque, types) for i in K]    
                
            
            # Mettre la cour
            fig = go.Figure(data=[go.Scatter(x=K, y=greeks)])
            return fig
    
@app.callback(
    Output('volatility_implicite-graph', 'figure'),
    Input("option-filter", "value"),
    Input("type-filter", "value"),
    Input("date", "date"),
    Input("s0-filter", "value"),
    Input("strike-filter", "value"),
    Input("rate-filter", "value"),
    Input("id_volatility", "children"),
)
def update_volatility_implicite(option, types, date, s0, strike, rate, sigma):
    if path != "/page1":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            df = pd.read_csv(f'src/data/clean_ListAllOptions{O.name}.csv')

            df['Maturity'] = pd.to_datetime(df['Maturity'], format="%Y-%m-%d")
            df['Maturity'] = df['Maturity'].apply(lambda x: x.strftime('%Y-%m-%d'))

            df['Maturity'] = df['Maturity'].apply(lambda x: get_relative_maturity(x))
            
        
            
            
            fig = px.scatter_3d(df, x='Strike', y='Maturity', z='implied Volatility')
            
            return fig







#### Callbacks straddle 
@app.callback(
    Output("s0-filter-str", "value"),
    Input("option-filter-str", "value"),
)
def update_s0_str(option):
    if path != "/page2":
        return no_update
    else: 
        O=Option(option,K=None,T=None)
        return O.S0

#callback for the volatility take the option and the type and return the volatility

@app.callback(
    Output("id_volatility_call", "children"),
    Output("id_volatility_put", "children"),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("strike-put-filter", "value"),
    Input("rate-filter-str", "value"),
    
)
def update_volatility_str(option, date, s0, strikec, strikep, rate):
    if path != "/page2":
        return no_update
    else :
        if s0 is None or strikec is None or strikep is None or rate is None:
            raise PreventUpdate
        else:
            C=Option(option,K=strikec,T=get_relative_maturity(date),r=rate)
            P=Option(option,K=strikep,T=get_relative_maturity(date),r=rate)
            Pc=Person("Call")
            Pp=Person("Put")
            opt_service=OptionsService()
            sigmac=opt_service.calcul_impl_volatility(C,Pc)
            sigmap=opt_service.calcul_impl_volatility(P,Pp)
            
            return round(sigmac[0],2), round(sigmap[0],2)
# Callback for the price take the option , the type and the sigma and return the price and the greeks

@app.callback(
    Output("id_price_str", "children"),
    Output('delta_str', 'children'),
    Output('gamma_str', 'children'),
    Output('vega_str', 'children'),
    Output('theta_str', 'children'),
    Output('rho_str', 'children'),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("strike-put-filter", "value"),
    Input("rate-filter-str", "value"),
    Input("id_volatility_call", "children"),
    Input("id_volatility_put", "children"),
)
def update_price_str(option, date, s0, strikec, strikep, rate, sigmac, sigmap):
    if path != "/page2":
        return no_update
    else:
        if s0 is None or strikec is None or strikep is None or rate is None or sigmac is None or sigmap is None:
            raise PreventUpdate
        else:
            C=Option(option,K=strikec,T=get_relative_maturity(date),r=rate)
            P=Option(option,K=strikep,T=get_relative_maturity(date),r=rate)
            Pc=Person("Call")
            Pp=Person("Put")

            
            bsm_str = BS_formula_Straddle(C, P, sigmac, sigmap)

            price = f"{bsm_str.BS_price():.2f} €"

            delta=f"{bsm_str.BS_delta():.2f}"

            gamma=f"{bsm_str.BS_gamma():.2f}"
            vega=f"{bsm_str.BS_vega():.2f}"
            theta=f"{bsm_str.BS_theta():.2f}"
            rho=f"{bsm_str.BS_rho():.2f}"
            
            return price, delta, gamma, vega, theta, rho

@app.callback(
    Output('greek-graph-str', 'figure'),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("strike-put-filter", "value"),
    Input("rate-filter-str", "value"),
    Input("id_volatility_call", "children"),
    Input("id_volatility_put", "children"),
    Input("grecque-filter-str", "value"),
    Input("min_S-filter-str", "value"),
    Input("max_S-filter-str", "value"),
)

def update_graph_str(option, date, s0, strikec, strikep, rate, sigmac, sigmap, grecque,min_S,max_S):
    """
    Représenter les grecs en fonction du prix du sous jacent
    Args:
        option (string): Nom de l'option
        date (string): Maturité
        s0 (string): Prix du sous jacent
        strikec (float): strike du call
        strikecp (float): strike du put
        rate (float): taux d'intérêt
        sigmac (float): volatilité du call
        sigmap (float): volatilité du put
        grecque (int): le grec à représenter
        min_S-max_S: La plage de valeurs de S
    """
    if path != "/page2":
        return no_update
    else:
        if s0 is None or strikec is None or strikep is None or rate is None or sigmac is None or sigmap is None:
            raise PreventUpdate
        else:
            C=Option(option,K=strikec,T=get_relative_maturity(date),r=rate)
            P=Option(option,K=strikep,T=get_relative_maturity(date),r=rate)

            T = get_relative_maturity(date)
            d1_c = (np.log(C.S0 / C.K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
            d2_c = d1_c - sigmac * np.sqrt(C.T)
            d1_p = (np.log(P.S0 / P.K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
            d2_p = d1_p - sigmap * np.sqrt(C.T)

            # Fonction qui calcule les greeks en fonction de S
            def greek(S,grecque):
                d1_c = (np.log(S / C.K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
                d2_c = d1_c - sigmac * np.sqrt(C.T)
                d1_p = (np.log(S / P.K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
                d2_p = d1_p - sigmap * np.sqrt(C.T)
                delta_c = norm.cdf(d1_c)
                delta_p = norm.cdf(d1_p)-1
                
        
                    # Gamma
                gamma_c = norm.pdf(d1_c) / (S * sigmac * np.sqrt(C.T))
                gamma_p = norm.pdf(d1_p) / (S * sigmap * np.sqrt(P.T))
        
                    # Vega
                vega_c = S * norm.pdf(d1_c) * np.sqrt(C.T)
                vega_p = S * norm.pdf(d1_p) * np.sqrt(P.T)
        
                    # Theta
                theta_c = -(S * norm.pdf(d1_c) * sigmac) / (2 * np.sqrt(C.T)) - C.r * C.K * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                theta_p = -(S * norm.pdf(d1_p) * sigmap) / (2 * np.sqrt(P.T)) + P.r * P.K * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
        
                    # Rho
                rho_c = C.K * C.T * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                rho_p = -P.K * P.T * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
                
                if grecque=="Delta":
                    return delta_c+delta_p
                elif grecque=="Gamma":
                    return gamma_c+gamma_p
                elif grecque=="Vega":
                    return vega_c+vega_p
                elif grecque=="Theta":
                    return theta_c+theta_p
                else: 
                    return rho_c+rho_p
                
            S = list(range(min_S,max_S))
            greeks = [greek(i,grecque) for i in S]    
                
            # Change the color in red
            fig = go.Figure(data=[go.Scatter(x=S, y=greeks, line=dict(color="red", width=2))])

            return fig
@app.callback(
    Output('strikec_final-graph_str', 'figure'),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("strike-put-filter", "value"),
    Input("rate-filter-str", "value"),
    Input("id_volatility_call", "children"),
    Input("id_volatility_put", "children"),
    Input("strikec_final-filter-str", "value"),
    Input("min_Kc-filter-str", "value"),
    Input("max_Kc-filter-str", "value"),
)

def update_strikec_str(option, date, s0, strikec, strikep, rate, sigmac, sigmap, grecque,min_K,max_K):
    if path != "/page2":
        return no_update
    else:
        if s0 is None or strikec is None or strikep is None or rate is None or sigmac is None or sigmap is None:
            raise PreventUpdate
        else:
            C=Option(option,K=strikec,T=get_relative_maturity(date),r=rate)
            P=Option(option,K=strikep,T=get_relative_maturity(date),r=rate)

            T = get_relative_maturity(date)
            d1_c = (np.log(C.S0 / C.K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
            d2_c = d1_c - sigmac * np.sqrt(C.T)
            d1_p = (np.log(P.S0 / P.K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
            d2_p = d1_p - sigmap * np.sqrt(C.T)

            # Fonction qui calcule les greeks en fonction de S
            def greek(K,grecque):
                d1_c = (np.log(C.S0 / K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
                d2_c = d1_c - sigmac * np.sqrt(C.T)
                d1_p = (np.log(P.S0 / P.K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
                d2_p = d1_p - sigmap * np.sqrt(C.T)
                delta_c = norm.cdf(d1_c)
                delta_p = norm.cdf(d1_p)-1
                
        
                    # Gamma
                gamma_c = norm.pdf(d1_c) / (C.S0 * sigmac * np.sqrt(C.T))
                gamma_p = norm.pdf(d1_p) / (P.S0 * sigmap * np.sqrt(P.T))
        
                    # Vega
                vega_c = C.S0 * norm.pdf(d1_c) * np.sqrt(C.T)
                vega_p = P.S0 * norm.pdf(d1_p) * np.sqrt(P.T)
        
                    # Theta
                theta_c = -(C.S0 * norm.pdf(d1_c) * sigmac) / (2 * np.sqrt(C.T)) - C.r * K * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                theta_p = -(P.S0 * norm.pdf(d1_p) * sigmap) / (2 * np.sqrt(P.T)) + P.r * P.K * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
        
                    # Rho
                rho_c = K * C.T * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                rho_p = -P.K * P.T * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
                
                if grecque=="Delta":
                    return delta_c+delta_p
                elif grecque=="Gamma":
                    return gamma_c+gamma_p
                elif grecque=="Vega":
                    return vega_c+vega_p
                elif grecque=="Theta":
                    return theta_c+theta_p
                else: 
                    return rho_c+rho_p
                
            K = list(range(min_K,max_K))
            greeks = [greek(i,grecque) for i in K]    
                
            # Change the color in red
            fig = go.Figure(data=[go.Scatter(x=K, y=greeks, line=dict(color="red", width=2))])

            return fig

@app.callback(
    Output('strikep_final-graph_str', 'figure'),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("strike-put-filter", "value"),
    Input("rate-filter-str", "value"),
    Input("id_volatility_call", "children"),
    Input("id_volatility_put", "children"),
    Input("strikep_final-filter-str", "value"),
    Input("min_Kp-filter-str", "value"),
    Input("max_Kp-filter-str", "value"),
)

def update_strikep_str(option, date, s0, strikec, strikep, rate, sigmac, sigmap, grecque,min_K,max_K):
    if path != "/page2":
        return no_update
    else:
        if s0 is None or strikec is None or strikep is None or rate is None or sigmac is None or sigmap is None:
            raise PreventUpdate
        else:
            C=Option(option,K=strikec,T=get_relative_maturity(date),r=rate)
            P=Option(option,K=strikep,T=get_relative_maturity(date),r=rate)

            T = get_relative_maturity(date)
            d1_c = (np.log(C.S0 / C.K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
            d2_c = d1_c - sigmac * np.sqrt(C.T)
            d1_p = (np.log(P.S0 / P.K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
            d2_p = d1_p - sigmap * np.sqrt(C.T)

            # Fonction qui calcule les greeks en fonction de S
            def greek(K,grecque):
                d1_c = (np.log(C.S0 / C.K) + (C.r + 0.5 * sigmac**2) * C.T) / (sigmac * np.sqrt(C.T))
                d2_c = d1_c - sigmac * np.sqrt(C.T)
                d1_p = (np.log(P.S0 / K) + (P.r + 0.5 * sigmap**2) * P.T) / (sigmap * np.sqrt(P.T))
                d2_p = d1_p - sigmap * np.sqrt(C.T)
                delta_c = norm.cdf(d1_c)
                delta_p = norm.cdf(d1_p)-1
                
        
                    # Gamma
                gamma_c = norm.pdf(d1_c) / (C.S0 * sigmac * np.sqrt(C.T))
                gamma_p = norm.pdf(d1_p) / (P.S0 * sigmap * np.sqrt(P.T))
        
                    # Vega
                vega_c = C.S0 * norm.pdf(d1_c) * np.sqrt(C.T)
                vega_p = P.S0 * norm.pdf(d1_p) * np.sqrt(P.T)
        
                    # Theta
                theta_c = -(C.S0 * norm.pdf(d1_c) * sigmac) / (2 * np.sqrt(C.T)) - C.r * C.K * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                theta_p = -(P.S0 * norm.pdf(d1_p) * sigmap) / (2 * np.sqrt(P.T)) + P.r * K * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
        
                    # Rho
                rho_c = C.K * C.T * np.exp(-C.r * C.T) * norm.cdf(d2_c)
                rho_p = -K * P.T * np.exp(-P.r * P.T) * norm.cdf(-d2_p)
                
                if grecque=="Delta":
                    return delta_c+delta_p
                elif grecque=="Gamma":
                    return gamma_c+gamma_p
                elif grecque=="Vega":
                    return vega_c+vega_p
                elif grecque=="Theta":
                    return theta_c+theta_p
                else: 
                    return rho_c+rho_p
                
            K = list(range(min_K,max_K))
            greeks = [greek(i,grecque) for i in K]    
                
            # Change the color in red
            fig = go.Figure(data=[go.Scatter(x=K, y=greeks, line=dict(color="red", width=2))])

            return fig



    
@app.callback(
    Output('volatility_implicite-graph-str', 'figure'),
    Input("option-filter-str", "value"),
    Input("date-str", "date"),
    Input("s0-filter-str", "value"),
    Input("strike-call-filter", "value"),
    Input("rate-filter-str", "value"),
    Input("id_volatility_call", "children"),
)
def update_volatility_implicite_call(option, date, s0, strike, rate, sigma):
    if path != "/page2":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            df = pd.read_csv(f'src/data/clean_ListAllOptions{O.name}.csv')

            df['Maturity'] = pd.to_datetime(df['Maturity'], format="%Y-%m-%d")
            df['Maturity'] = df['Maturity'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df['Maturity'] = df['Maturity'].apply(lambda x: get_relative_maturity(x))
            
            
            fig = px.scatter_3d(df, x='Strike', y='Maturity', z='implied Volatility')
            
            return fig







#callback for the volatility take the option and the type and return the volatility
@app.callback(
    Output("discount_t1_fix", "children"),
    Output("discount_tn_fix", "children"),
    Output("discount_t1_var", "children"),
    Output("discount_tn_var", "children"),
    Input("direction", "value"),
    Input("notionnel", "value"),
    Input("date-pr-sw", "date"),
    Input("val-date-sw", "date"),
    Input("date-sw", "date"),
    Input("discountindex", "value"),
    Input("fixed_frequency", "value"),
    Input("float_frequency", "value"),
    Input("fixed_rate_sw_1", "value"),

)

def update_swap_price(direction, notional, valuationdate, valuedate, maturity, discountindex, fixed_frequency, float_frequency, fixed_rate):
    if path != "/page3":
        return no_update
    else:
        if valuationdate is None or valuedate is None or maturity is None or fixed_frequency is None or float_frequency is None or fixed_rate is None or direction is None or notional is None:
            raise PreventUpdate
        else:
            maturitydate = pd.to_datetime(maturity, format="%Y-%m-%d")
            valuationdate = pd.to_datetime(valuationdate, format="%Y-%m-%d")
            valuedate = pd.to_datetime(valuedate, format="%Y-%m-%d")
            swap = Swap(direction, notional, fixed_rate, maturitydate, valuedate, float_frequency, fixed_frequency)
            swappricer = SwapPricer(swap, valuationdate)
            discountrate1_fix = f'{swappricer.DiscountRate(valuedate, fixed_frequency):.2f}'
            discountraten_fix = f'{swappricer.DiscountRate(maturitydate, fixed_frequency):.2f}'
            discountrate1_var = f'{swappricer.DiscountRate(valuedate, float_frequency):.2f}'
            discountraten_var = f'{swappricer.DiscountRate(maturitydate, float_frequency):.2f}'
            return discountrate1_fix, discountraten_fix, discountrate1_var, discountraten_var


@app.callback(
    Output("id_price_sw", "children"),
    Output("pv_fix", "children"),
    Output("pv_float", "children"),
    Input("direction", "value"),
    Input("notionnel", "value"),
    Input("date-pr-sw", "date"),
    Input("val-date-sw", "date"),
    Input("date-sw", "date"),
    Input("discountindex", "value"),
    Input("fixed_frequency", "value"),
    Input("float_frequency", "value"),
    Input("fixed_rate_sw_1", "value"),

)

def update_swap_price(direction, notional, valuationdate, valuedate, maturity, discountindex, fixed_frequency, float_frequency, fixed_rate):
    if path != "/page3":
        return no_update
    else:
        if valuationdate is None or valuedate is None or maturity is None or fixed_frequency is None or float_frequency is None or fixed_rate is None or direction is None or notional is None:
            raise PreventUpdate
        else:
            maturitydate = pd.to_datetime(maturity, format="%Y-%m-%d")
            valuationdate = pd.to_datetime(valuationdate, format="%Y-%m-%d")
            swap = Swap(direction, notional, fixed_rate, maturitydate, valuedate, float_frequency, fixed_frequency)
            swappricer = SwapPricer(swap, valuationdate)
            price = f'{-swappricer.swap_price():.2f}'
            fixed_pv = f"{swappricer.LegPV('fixed', notional):.2f}"
            float_pv = f"{swappricer.LegPV('float', notional):.2f}"
            return price, fixed_pv, float_pv



## Callbacks page4 

@app.callback(
    Output("s0-asian-filter", "value"),
    Input("option-asian-filter", "value"),
    Input("type-asian-filter", "value"),
)
def update_s0(option, types):
    if path != "/page4":
        return no_update
    else:
        O=Option(option,K=None,T=None)
        return  O.S0

#callback for the volatility take the option and the type and return the volatility

@app.callback(
    Output("hist_volatility", "children"),
    Input("option-asian-filter", "value"),
    Input("type-asian-filter", "value"),
    Input("asian_date", "date"),
    Input("s0-asian-filter", "value"),
    Input("strike-asian-filter", "value"),
    Input("rate-asian-filter", "value"),
    
)
def update_volatility(option, types, date, s0, strike, rate):
    if path != "/page4":
        return no_update
    else:    
        if s0 is None or strike is None or rate is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            P=Person(types)
            opt_service=OptionsService()

            hist_sigma=opt_service.calcul_hist_volatility(O,P)
            
            return round(hist_sigma,2)


@app.callback(
    Output("id_asian_price", "children"),
    Output('asian_delta', 'children'),
    Output('asian_gamma', 'children'),
    Output('asian_vega', 'children'),
    Input("option-asian-filter", "value"),
    Input("type-asian-filter", "value"),
    Input("asian_date", "date"),
    Input("s0-asian-filter", "value"),
    Input("strike-asian-filter", "value"),
    Input("rate-asian-filter", "value"),
    Input("hist_volatility", "children"),
    Input("n_simul-filter", "value"),
    Input("fen-filter", "value"),
)
def update_price(option, types, date, s0, strike, rate, sigma, n_simul, fen):
    if path != "/page4":
        return no_update
    else:
        if s0 is None or strike is None or rate is None or sigma is None or n_simul is None or fen is None:
            raise PreventUpdate
        else:
            O=Option(option,K=strike,T=get_relative_maturity(date),r=rate)
            P=Person(types)
            
            As_price = AsianMCPricer( O, P,float(sigma), n_simul, fen)
            price = f"{As_price.MC_price(s0, sigma):.2f} €"

            delta=f"{As_price.MC_delta():.2f}"

            gamma=f"{As_price.MC_gamma():.2f}"
            vega=f"{As_price.MC_vega():.2f}"
            
            return price, delta, gamma, vega




if __name__ == "__main__":
    app.run_server(debug=True)

