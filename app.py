import os
import threading

import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from utils import draw_plot, LIST_OF_TICKERS, DATA, generate_data

CURRENT_TICKER = None

FIG = go.Figure(
    layout=dict(
        title=dict(
            text='Price: 0',
            font=dict(size=30, color='rgb(57, 247, 171)')
        ),
        xaxis=dict(
            title='time',
            autorange=True,
            showline=False,
            color='rgb(57, 247, 171)',  # label color
            showgrid=True,
            minor=dict(showgrid=True),
        ),
        yaxis=dict(
            title='price',
            autorange=True,
            showline=False,
            color='rgb(57, 247, 171)',
            showgrid=False,
            zeroline=True,
            zerolinecolor='rgb(57, 247, 171)',
            zerolinewidth=0.1,
        ),
        paper_bgcolor='rgb(31,38,48)',
        plot_bgcolor='rgb(31,38,48)',
    )
)

app = Dash(
    __name__,
    assets_folder=os.path.join(os.path.dirname(__file__), 'assets')
)

app.layout = html.Div(
    className='general',
    children=[
        html.Div(
            className='title',
            children=[
                html.P('Price change in real time', className='head')
            ]
        ),
        html.Div(
            className='tickers',
            children=[
                dcc.Dropdown(
                    id="ticker",
                    # value='ticker_0',  # select by default
                    options=LIST_OF_TICKERS,
                    placeholder='Ticker',
                    searchable=True,
                    maxHeight=100,
                    optionHeight=20,
                ),
            ]
        ),
        html.Div(
            className='plot',
            children=[
                dcc.Graph(id='graph', animate=True),
                dcc.Interval(
                    id='interval-component',
                    disabled=True,
                    max_intervals=-1,
                    interval=1*1000,  # update every seconds
                    n_intervals=0
                )
            ]
        )
    ]
)


@app.callback(
    output=Output('graph', 'figure'),
    inputs=dict(
        ticker=Input('ticker', 'value'),
        n=Input('interval-component', 'n_intervals')
    )
)
def update_plot(ticker, n):
    global CURRENT_TICKER
    if not ticker:
        return FIG

    if CURRENT_TICKER != ticker:
        CURRENT_TICKER = ticker
        FIG.data = tuple()

    FIG.add_trace(draw_plot(DATA[ticker], DATA['times']))
    FIG.update_layout(
        title=dict(
            text=f'PRICE = {DATA[ticker][-1]}',
            font=dict(color='red' if DATA[ticker][-1] < 0 else 'rgb(128, 255, 159)')
        ),
    )
    return FIG


@app.callback(
    Output('interval-component', 'disabled'),
    [Input('ticker', 'value')]
)
def stop_interval(ticker):
    """If the ticker is not transferred or deleted, stop updating the graph."""
    disabled = True if not ticker else False
    return disabled


if __name__ == '__main__':
    t = threading.Thread(target=generate_data)
    t.start()

    app.run_server(port=8000, host='0.0.0.0', debug=True)
