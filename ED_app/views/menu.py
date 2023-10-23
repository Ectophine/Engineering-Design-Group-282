from dash import dcc, html
from ..config import timeline, usage, view


def make_menu_layout():
    return (
        html.Div(
            className='card',
            children=[
                html.H3("Adjust your dashboard"),
                html.H4("Timeline"),
                dcc.RadioItems(
                    id="select-timeline",
                    options=[{"label": i, "value": i} for i in timeline],
                    value=timeline[0],
                ),
                html.H4("Usage"),
                dcc.RadioItems(
                    id="select-usage",
                    options=[{"label": i, "value": i} for i in usage],
                    value=usage[0],
                ),
                html.H4("View"),
                dcc.RadioItems(
                    id="select-view",
                    options=[{"label": i, "value": i} for i in view],
                    value=view[0],
                )
            ]
        )
    )
