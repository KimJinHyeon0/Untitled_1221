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


def generate_start_time() -> int:
    return random.randint(Config.min_start_time, Config.max_start_time)


def generate_elapsed_time() -> int:
    return random.randint(Config.min_elapsed_time, Config.max_elapsed_time)


@dataclass
class Delivery:
    id: str = field(default_factory=generate_id_delivery)

    src_lat: float = field(default_factory=generate_lat)
    src_lon: float = field(default_factory=generate_lon)

    dst_lat: float = field(default_factory=generate_lat)
    dst_lon: float = field(default_factory=generate_lon)

    baggage: int = field(default_factory=generate_baggage)

    start_time: int = field(default_factory=generate_start_time)
    elapsed_time: int = field(default_factory=generate_elapsed_time)
    end_time: int = field(init=False, default=0)

    assigned: str = field(default_factory=str)

    def __post_init__(self):
        self.end_time = self.start_time + self.elapsed_time



@dataclass
class Pro:
    id: str = field(default_factory=generate_id_pro)

    pre_lat: float = field(default_factory=generate_lat)
    pre_lon: float = field(default_factory=generate_lon)

    max_cap: int = field(default_factory=generate_capacity)
    cur_cap: int = field(default=0)

    completed: list = field(default_factory=list)


def visualize(deliveries, pros):
    data = []
    layout = go.Layout(title='test',
                       mapbox=dict(
                           center={"lat": 37.563383, "lon": 126.996039},
                           style="carto-positron",
                           zoom=10.5)
                       )

    # Delivery
    for row in deliveries.itertuples():
        data.append(go.Scattermapbox(
            name=f'Delivery_{row.id}',
            mode="markers+text+lines",
            lon=[row.src_lon, row.dst_lon],
            lat=[row.src_lat, row.dst_lat],
            legendgroup='group',
            legendgrouptitle=dict(text='Delivery'),
            hovertemplate=[
                '<br>'.join([
                    f'Source',
                    f'Baggage: {row.baggage}',
                    f'Pickup time: {str(row.start_time // 60).zfill(2)}:{str(row.start_time % 60).zfill(2)}',
                    f'Elapsed time: {row.elapsed_time}m',
                    f'Expire time: {str(row.end_time // 60).zfill(2)}:{str(row.end_time % 60).zfill(2)}',
                ]),
                '<br>'.join([
                    f'Destination',
                    f'Baggage: {row.baggage}',
                    f'Pickup time: {str(row.start_time // 60).zfill(2)}:{str(row.start_time % 60).zfill(2)}',
                    f'Elapsed time: {row.elapsed_time}m',
                    f'Expire time: {str(row.end_time // 60).zfill(2)}:{str(row.end_time % 60).zfill(2)}',
                ]),
            ],
            marker=dict(size=15, color=['blue', 'red']),
            line=dict(color='grey'),
        ))

    # Pro
    for row in pros.itertuples():
        data.append(go.Scattermapbox(
            name=f'Pro_{row.id}',
            mode="markers",
            lon=[row.pre_lon],
            lat=[row.pre_lat],
            legendgroup='group2',
            legendgrouptitle=dict(text='Pro'),
            hovertemplate=f'Capability : {row.cur_cap}/{row.max_cap}',
            marker=dict(size=15, color='orange'),
        ))

    fig = go.Figure(data=data, layout=layout)
    fig.show()
