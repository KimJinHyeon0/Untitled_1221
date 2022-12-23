from configs import Config
from dataclasses import dataclass, field
import plotly.graph_objects as go
import random
import string
import pandas as pd
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2) -> float:
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return round(c * r, 2)


def generate_random_coor(lon1, lat1, time):
    lon_per_km = 0.00901
    lat_per_km = 0.01126
    dlon = min(lon_per_km * Config.max_distance, time * Config.speed_limit / 60)
    dlat = min(lat_per_km * Config.max_distance, time * Config.speed_limit / 60)

    lon2, lat2 = 0, 0
    while not (Config.min_distance <= haversine(lon1, lat1, lon2, lat2) <= Config.max_distance):
        lon2 = random.uniform(lon1 - dlon, lon1 + dlon)
        lat2 = random.uniform(lat1 - dlat, lat1 + dlat)

    return lon2, lat2


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


def min2clock(x):
    return f'{str(x // 60).zfill(2)}:{str(x % 60).zfill(2)}'


def distance2time(x):
    return round(x / Config.speed_limit * 60)


def visualize(deliveries, pros):
    data = []
    layout = go.Layout(title='test',
                       mapbox=dict(
                           center={"lat": 37.563383, "lon": 126.996039},
                           style="carto-positron",
                           zoom=10.5),
                       hovermode='closest',
                       legend=dict(groupclick='toggleitem'),
                       )

    # Delivery
    for row in deliveries.itertuples():
        data.append(go.Scattermapbox(
            name=f'Delivery_{row.id}',
            mode="markers+text+lines",
            lon=[row.src_lon, row.dst_lon],
            lat=[row.src_lat, row.dst_lat],
            legendgroup='group',
            legendgrouptitle=dict(font=dict(size=15), text='Delivery'),
            hovertemplate=[
                '<br>'.join([
                    f'Source',
                    f'Distance: {row.distance}km',
                    f'Estimated time: {row.estimated}min',
                    f'Baggage: {row.baggage}',
                    f'Pickup time: {min2clock(row.start_time)}',
                    f'Interval time: {row.interval_time}min',
                    f'Expire time: {min2clock(row.end_time)}',
                ]),
                '<br>'.join([
                    f'Destination',
                    f'Distance: {row.distance}km',
                    f'Estimated time: {row.estimated}min',
                    f'Baggage: {row.baggage}',
                    f'Pickup time: {min2clock(row.start_time)}',
                    f'Interval time: {row.interval_time}min',
                    f'Expire time: {min2clock(row.end_time)}',
                ]),
            ],
            marker=dict(size=15, color=['blue', 'red']),
            line=dict(color='grey'),
            opacity=0.5,
        ))

    # Pro
    for row in pros.itertuples():
        data.append(go.Scattermapbox(
            name=f'Pro_{row.id}',
            mode="markers",
            lon=[row.pre_lon],
            lat=[row.pre_lat],
            legendgroup='group2',
            legendgrouptitle=dict(font=dict(size=15), text='Pro'),
            hovertemplate='<br>'.join([
                    f'Capacity: {row.cur_cap}/{row.max_cap}',
                    f'Completed : {row.completed}',
                    f'Num.Completed : {len(row.completed)}',
                ]),
            marker=dict(size=15, color='orange'),
        ))

    fig = go.Figure(data=data, layout=layout)
    fig.show()