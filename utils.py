import random
import time
from datetime import timedelta, datetime

import plotly.graph_objects as go

LIST_OF_TICKERS = [f'ticker_{n}' for n in range(100)]
DATA = {ticker: [0] for ticker in LIST_OF_TICKERS}

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATA['times'] = [datetime.strptime(datetime.now().strftime(TIME_FORMAT), TIME_FORMAT)]


def generate_movement():
    """Generate random movement."""
    movement = -1 if random.random() < 0.5 else 1
    return movement


def generate_data():
    """Each second generate artificial price and time"""
    global DATA, LIST_OF_TICKERS
    while True:
        DATA['times'].append(DATA['times'][-1] + timedelta(seconds=1))
        for ticker in LIST_OF_TICKERS:
            DATA[ticker].append(DATA[ticker][-1] + generate_movement())
        time.sleep(1)


def draw_plot(price: list, times: list):
    """
    Create plotly.graph_objs._deprecations.Line and return

    Parameters
    ----------
    price : list of prices
    times : list of times
    """
    x = times + [times[-1] + timedelta(seconds=sec) for sec in range(1, 6)]
    y = price + [None] * 5
    fig = go.Line(
        x=x,
        y=y,
        showlegend=False,
        line=dict(color='red')
    )

    return fig
