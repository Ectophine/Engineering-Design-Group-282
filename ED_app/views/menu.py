from dash import dcc, html
from ..config import timeline, usage, view
def generate_description_card():
    return html.Div(
        id='description-card',
        children=[
            html.H5("Input Panel"),
            html.Div(
                id="intro",
                children=' ',
            )
        ]
    )

def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            html.Label("Timeline"),
            dcc.Dropdown(
                id="select-timeline",
                options=[{"label": i, "value": i} for i in timeline],
                value=timeline[0],
            ),
            html.Br(),
            html.Label("Usage"),
            dcc.Dropdown(
                id="select-usage",
                options=[{"label": i, "value": i} for i in usage],
                value=usage[0],
            ),
            html.Label("View"),
            dcc.Dropdown(
                id="select-view",
                options=[{"label": i, "value": i} for i in view],
                value=view[0],
            ),
        ], style={"textAlign": "float-left"}
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card()]