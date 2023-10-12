from ED_app.main import app
from ED_app.views.linegraph import Linegraph
from ED_app.views.menu import make_menu_layout
from ED_app.data import get_data, change_timeline, calculate_savings
from dash import html
from dash.dependencies import Input, Output
from ED_app.cost import liters_conversion, temperature_conversion
from ED_app.randomstatement import random_statement

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

        df['Water Cost'] = liters_conversion(df['Water Usage'], 'money')
        df['Gas Usage'] = temperature_conversion(df['Temperature'], df['Water Usage'], 'gas')
        df['Gas Cost'] = temperature_conversion(df['Temperature'], df['Water Usage'], 'money')

        df = calculate_savings(df)

        df_after_baseline = df.loc[7:]
        total_water_use_savings = df_after_baseline['Water Usage Savings'].sum()
        total_gas_use_savings = df_after_baseline['Gas Usage Savings'].sum()
        total_water_cost_savings = df_after_baseline['Water Cost Savings'].sum()
        total_gas_cost_savings = df_after_baseline['Gas Cost Savings'].sum()

        linegraph = Linegraph("Line Graph", 'Date', 'Water Usage', df)

        random_statement = random_statement(df, total_water_use_savings, total_gas_use_savings)

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
                        ),
                        html.Div(
                            id='random-statement',
                            children=html.H3(random_statement)
                        ),
                        html.Div(
                            id='savings-boxes',
                            children=[
                                html.Div(id='water-use-savings',
                                         children=[html.H4('You saved'),
                                                   html.H3(total_water_use_savings),
                                                   html.H4('liters of water so far!')]),
                                html.Div(id='gas-use-savings',
                                         children=[html.H4('You saved'),
                                                   html.H3(total_gas_use_savings),
                                                   html.H4('cubic meters of gas so far!')]),
                                html.Div(id='water-cost-savings',
                                         children=[html.H4('You saved'),
                                                   html.H3(total_water_cost_savings),
                                                   html.H4('euro in water so far!')]),
                                html.Div(id='gas-cost-savings',
                                         children=[html.H4('You saved'),
                                                   html.H3(total_gas_cost_savings),
                                                   html.H4('euro in gas so far!')]),
                            ]
                        )
                    ]
                )
            ]
        )


        @app.callback(
            Output(linegraph.html_id, 'figure'),
            Input("select-timeline", "value"),
            Input("select-usage", 'value'),
            Input('select-view', 'value')
        )
        def update_plot(timeline, usage, view):
            # Filters the df based on the chosen timeline
            new_df = df
            if timeline != 'Daily':
                new_df = change_timeline(df, timeline)

            # Generates a graph with two lines based on inputs
            if usage == 'Both':
                return linegraph.generate_both_linegraph(new_df, view)

            # Generates a graph with one line based on inputs
            if view == 'Amount':
                return linegraph.generate_linegraph(new_df, usage)
            elif view == 'Cost':
                if usage == 'Water Usage':
                    return linegraph.generate_linegraph(new_df, 'Water Cost')
                elif usage == 'Gas Usage':
                    return linegraph.generate_linegraph(new_df, 'Gas Cost')
            return linegraph.generate_linegraph(new_df, 'Water Usage')

    app.run_server(debug=False, dev_tools_ui=False)
