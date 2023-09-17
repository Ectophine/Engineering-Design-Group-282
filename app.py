from ED_app.main import app
from ED_app.views.menu import make_menu_layout
from dash import html
from dash.dependencies import Input, Output

if __name__ == '__main__':
    #df = get_data()

    app.layout = html.Div(
        id='app_container',
        children=[
            # Left column
            html.Div(
                id='left-column',
                className='three columns',
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id='right-column',
                className="nine columns",
                children=[
                    ' '
                ]
            )
        ]
    )

    app.run_server(debug=False, dev_tools_ui=False)