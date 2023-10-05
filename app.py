from ED_app.main import app
from ED_app.views.linegraph import Linegraph
from ED_app.views.menu import make_menu_layout
from ED_app.data import get_data, set_baseline
from dash import html
from dash.dependencies import Input, Output

if __name__ == '__main__':
    df = get_data()
    data_count = len(df)
    if data_count < 7:
        app.layout = html.Div(
            id='app_container',
            children=[
                html.H1(
                    id='title',
                    children='Water Sensor Dashboard'
                ),
                html.H3(
                    id='sub-title',
                    children='''
                            Track your water and power usage while showering over time!
                        '''),
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
                    children=[html.H3(
                        id='baseline-reminder',
                        children='''
                        The app is still calculating your baseline. Keep showering normally with the shower
                        sensor attached, and check back later to track your usage! The dashboard will be available after
                        7 showers.
                        '''
                    )
                    ]
                )
            ]
        )
    else:
        progress_water = df.iloc[data_count - 1][1] - df.iloc[data_count - 2][1]
        if progress_water > 0:
            progress_water_str = str(progress_water)
            progress_statement = 'You used ' + progress_water_str + (
                ' more liter(s) of water this shower than last time. Try taking'
                ' a shorter shower next time!')
        elif progress_water < 0:
            progress_water_str = str(abs(progress_water))
            progress_statement = 'You used ' + progress_water_str + (
                ' less liter(s) of water this shower than last time.'
                ' Great job!')
        else:
            progress_statement = 'You used the same amount of water this shower as last time.'

        df['Water Cost'] = df['Water Usage'] * 2.50
        df['Power Cost'] = df['Power Usage'] * 3.50

        linegraph = Linegraph("Line Graph", 'Date', 'Water Usage', df)
        app.layout = html.Div(
            id='app_container',
            children=[
                html.H1(
                    id='title',
                    children='Water Sensor Dashboard'
                ),
                html.H3(
                    id='sub-title',
                    children='''
                    Track your water and power usage while showering over time!
                '''),
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
                        linegraph,
                        html.Div(
                            id='progress-statement',
                            children=html.H3(progress_statement)
                        )
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
            if view == 'Amount':
                return linegraph.generate_linegraph(df, usage)
            elif view == 'Cost':
                if usage == 'Water Usage':
                    return linegraph.generate_linegraph(df, 'Water Cost')
                elif usage == 'Power Usage':
                    return linegraph.generate_linegraph(df, 'Power Cost')
            return linegraph.generate_linegraph(df, 'Water Usage')

    app.run_server(debug=False, dev_tools_ui=False)
