from ED_app.main import app
from ED_app.views.linegraph import Linegraph
from ED_app.views.menu import make_menu_layout
from ED_app.data import get_data
from dash import html
from dash.dependencies import Input, Output

if __name__ == '__main__':
    df = get_data()

    linegraph = Linegraph("Line Graph", 'Date', 'Water Usage', df)
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
                    linegraph
                ]
            )
        ]
    )

    # Filters data based on input panel
    # def filter_data(timeline, usage, view):
    #     filtered_df = df
    #
    #     # if timeline != '':
    #         # filtered_df = filtered_df[filtered_df'']
    #     if usage != '':
    #         filtered_df

    @app.callback(
        Output(linegraph.html_id, 'figure'),
        Input("select-timeline", "value"),
        Input("select-usage", 'value'),
        Input('select-view', 'value')
    )
    def update_plot(timeline, usage, view):
        if usage == '':
            return linegraph.generate_linegraph(df, 'Water Usage')
        elif usage != 'Both':
            return linegraph.generate_linegraph(df, usage)
        return linegraph.generate_linegraph(df, 'Water Usage')

    app.run_server(debug=False, dev_tools_ui=False)
