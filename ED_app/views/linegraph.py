from dash import dcc, html
import plotly.express as px


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

        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select'
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        self.fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y
        )

        return self.fig

    def generate_both_linegraph(self, new_dataframe, view):
        self.df = new_dataframe
        if view == 'Amount':
            self.fig = px.line(new_dataframe, x='Date', y=['Water Usage', 'Gas Usage'])
            self.feature_y = 'Usage'
        elif view == 'Cost':
            self.fig = px.line(new_dataframe, x='Date', y=['Water Cost', 'Gas Cost'])
            self.feature_y = 'Cost'

        self.feature_x = 'Date'

        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select'
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        self.fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y
        )

        return self.fig
