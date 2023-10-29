from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class Linegraph(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        super().__init__(
            className='graph_card',
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ]
        )

    def generate_linegraph(self, new_dataframe, usage):
        self.df = new_dataframe
        self.fig = px.line(new_dataframe, x=new_dataframe['Date'], y=new_dataframe[usage])

        self.feature_x = 'Date'
        self.feature_y = usage

        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select',
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
        )

        return self.fig

    def generate_both_linegraph(self, new_dataframe, view):
        self.df = new_dataframe
        self.fig = go.Figure()
        if view == 'Amount':
            self.fig.add_trace(
                go.Scatter(x=new_dataframe['Date'], y=new_dataframe['Water Usage'], mode='lines', name='Water '
                                                                                                       'Usage'))
            self.fig.add_trace(
                go.Scatter(x=new_dataframe['Date'], y=new_dataframe['Gas Usage'], mode='lines', name='Gas Usage',
                           yaxis='y2'))

            self.fig.update_layout(
                yaxis=dict(title='Water Usage'),
                yaxis2=dict(title='Gas Usage', overlaying='y', side='right')
            )

            self.feature_y = 'Usage'

        elif view == 'Cost':
            self.fig.add_trace(
                go.Scatter(x=new_dataframe['Date'], y=new_dataframe['Water Cost'], mode='lines', name='Water '
                                                                                                      'Cost'))
            self.fig.add_trace(
                go.Scatter(x=new_dataframe['Date'], y=new_dataframe['Gas Cost'], mode='lines', name='Gas Cost',
                           yaxis='y2'))

            self.fig.update_layout(
                yaxis=dict(title='Water Cost'),
                yaxis2=dict(title='Gas Cost', overlaying='y', side='right')
            )

            self.feature_y = 'Cost'

        self.feature_x = 'Date'

        self.fig.update_xaxes(fixedrange=True)

        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select',
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y
        )

        return self.fig
