from configs import Config
from dataclasses import dataclass, field
import plotly.graph_objects as go
import random
import string
import pandas as pd


def generate_id_delivery() -> str:
    return "".join(random.choices(string.digits, k=Config.id_length_delivery))


def generate_id_pro() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=Config.id_length_pro))


def generate_capacity() -> int:
    return random.randint(Config.min_capacity, Config.max_capacity)


def generate_baggage() -> int:
    return random.randint(Config.min_baggage, Config.max_baggage)


def generate_lat() -> float:
    return random.uniform(Config.min_lat, Config.max_lat)


def generate_lon() -> float:
    return random.uniform(Config.min_lon, Config.max_lon)

@dataclass
class Delivery:
    id: str = field(default_factory=generate_id_delivery)

    src_lat: float = field(default_factory=generate_lat)
    src_lon: float = field(default_factory=generate_lon)

    dst_lat: float = field(default_factory=generate_lat)
    dst_lon: float = field(default_factory=generate_lon)
    baggage: int = field(default_factory=generate_baggage)


@dataclass
class Pro:
    id: str = field(default_factory=generate_id_pro)

    pre_lat: float = field(default_factory=generate_lat)
    pre_lon: float = field(default_factory=generate_lon)

    max_cap: int = field(default_factory=generate_capacity)
    cur_cap: int = field(default=0)


def visualize(df1, df2):
    scatter = go.Scattermapbox(
        lat=df2.pre_lat,
        lon=df2.pre_lon,
        mode='markers',
        hovertext=df2.id,
        hoverinfo='all',
        marker=dict(size=20, color='orange'),
        selected=dict(marker=dict(size=20, color='blue'))
    )

    layout = go.Layout(title='test',
                       mapbox=dict(
                           center={"lat": 37.563383, "lon": 126.996039},
                           style="carto-positron",
                           zoom=10.5))

    fig = go.Figure(data=[scatter], layout=layout)

    for row in df1.itertuples():
        fig.add_trace(go.Scattermapbox(
            mode="markers+text+lines",
            lon=[row.src_lon, row.dst_lon],
            lat=[row.src_lat, row.dst_lat],
            hovertext=f'Delivery_id : {row.id}',
            hoverinfo='all',
            marker=dict(size=10, color=['blue', 'red']))
        )

    fig.show()