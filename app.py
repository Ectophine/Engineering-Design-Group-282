from ED_app.main import app
from ED_app.views.linegraph import Linegraph
from ED_app.views.menu import make_menu_layout
from ED_app.data import get_data, change_timeline, calculate_savings, FileModifiedHandler
from dash import html, dcc
from dash.dependencies import Input, Output
from ED_app.cost import liters_conversion, temperature_conversion
from ED_app.randomstatement import random_statement
from watchdog.observers import Observer
import ED_app.config

if __name__ == '__main__':
    df = get_data()
    data_count = len(df)
    if data_count < 7:
        app.layout = html.Div(
            id='app_container',
            children=[
                html.Div(
                    className='header',
                    children=[
                        html.Img(src=r'assets/watersensorlogo.png'),
                        html.Div(
                            className='title-bar',
                            children=[
                                html.H1(
                                    id='title',
                                    children='Water Sensor Dashboard'
                                ),
                                html.H2(
                                    id='sub-title',
                                    children='''
                                            Track your water and power usage while showering over time!
                                        ''')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='main columns',
                    children=[
                        html.Div(
                            className='menu',
                            children=html.Div(
                                className='card',
                                children=[
                                    html.H3("Adjust your dashboard"),
                                    html.Span("No adjustments available"),
                                ]
                            )
                        ),
                        html.Div(
                            className="data",
                            children=html.Div(
                                className='card',
                                children=html.H4(ED_app.config.no_data_text)
                            )
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
        df['Gas Usage'] = temperature_conversion(df['Temperature'], df['Water Usage'], 'gas')  # df['Date'])
        df['Gas Cost'] = temperature_conversion(df['Temperature'], df['Water Usage'], 'money')  # df['Date'])

        df = calculate_savings(df)

        df_after_baseline = df.loc[7:]
        total_water_use_savings = round(df_after_baseline['Water Usage Savings'].sum(), 2)
        total_gas_use_savings = round(df_after_baseline['Gas Usage Savings'].sum(), 2)
        total_water_cost_savings = round(df_after_baseline['Water Cost Savings'].sum(), 2)
        total_gas_cost_savings = round(df_after_baseline['Gas Cost Savings'].sum(), 2)

        linegraph = Linegraph("Line Graph", 'Date', 'Water Usage', df)

        random_statement = random_statement(df, total_water_use_savings, total_gas_use_savings)

        app.layout = html.Div(
            id='app_container',
            children=[
                html.Div(
                    className='header',
                    children=[
                        html.Img(src=r'assets/watersensorlogo.png'),
                        html.Div(
                            className='title-bar',
                            children=[
                                html.H1(
                                    id='title',
                                    children='Water Sensor Dashboard'
                                ),
                                html.H2(
                                    id='sub-title',
                                    children='''
                                    Track your water and power usage while showering over time!
                                ''')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='main columns',
                    children=[
                        # Left column
                        html.Div(
                            className='menu',
                            children=make_menu_layout()
                        ),

                        # Right column
                        html.Div(
                            className="data",
                            children=[
                                html.Div(
                                    className='card',
                                    children=linegraph
                                ),
                                html.Div(
                                    className='columns two',
                                    children=[
                                        html.Div(
                                            className='card',
                                            children=html.Div(
                                                id='progress-statement',
                                                className='statement',
                                                children=html.H4(progress_statement)
                                            )
                                        ),
                                        html.Div(
                                            className='card',
                                            children=html.Div(
                                                id='random-statement',
                                                className='statement',
                                                children=html.H4(random_statement)
                                            )
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='columns four savings-boxes',
                                    children=[
                                        html.Div(
                                            className='card',
                                            children=[
                                                html.Img(src=r'assets/water.png'),
                                                html.Div(
                                                    id='water-use-savings',
                                                    children=[
                                                        html.H3(total_water_use_savings),
                                                        html.Span('Liters of water saved')
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='card',
                                            children=[
                                                html.Img(src=r'assets/money.png'),
                                                html.Div(
                                                    id='water-cost-savings',
                                                    children=[
                                                        html.H3(total_water_cost_savings),
                                                        html.Span('Euro\'s saved on water')
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='card',
                                            children=[
                                                html.Img(src=r'assets/gas.png'),
                                                html.Div(
                                                    id='gas-use-savings',
                                                    children=[
                                                        html.H3(total_gas_use_savings),
                                                        html.Span('m\u00b2 of gas saved')
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='card',
                                            children=[
                                                html.Img(src=r'assets/money.png'),
                                                html.Div(
                                                    id='gas-cost-savings',
                                                    children=[
                                                        html.H3(total_gas_cost_savings),
                                                        html.Span('Euro\'s saved on gas')
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dcc.Interval(id='live-updates',
                                             interval=5000,
                                             n_intervals=0)
                            ]
                        )
                    ]
                )

            ]
        )


        @app.callback(
            Output(linegraph.html_id, 'figure'),
            Input("select-timeline", 'value'),
            Input("select-usage", 'value'),
            Input('select-view', 'value'),
            Input('live-updates', 'n_intervals')
        )
        def update_plot(timeline, usage, view, n_intervals):
            # Filters the df based on the chosen timeline
            new_df = get_data()
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

    # This code checks for file updates in the sensor log and appends it to the stored data
    # This will run indefinitely so long the app is running, and can be stopped by using Ctrl+C

    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path='ED_app/data/log/', recursive=False)
    observer.start()

    app.run_server(debug=True, dev_tools_ui=False)
