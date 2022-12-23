from configs import Config
from utils import *
from model import Model

@dataclass
class Delivery:
    id: str = field(default_factory=generate_id_delivery)

    src_lon: float = field(default_factory=generate_lon)
    src_lat: float = field(default_factory=generate_lat)

    dst_lon: float = field(init=False)
    dst_lat: float = field(init=False)

    distance: float = field(init=False)

    baggage: int = field(default_factory=generate_baggage)

    start_time: int = field(default_factory=generate_start_time)
    interval_time: int = field(default_factory=generate_elapsed_time)
    end_time: int = field(init=False)
    estimated: int = field(init=False)

    assigned: str = field(default_factory=str)

    def __post_init__(self):
        self.dst_lon, self.dst_lat = generate_random_coor(self.src_lon, self.src_lat, self.interval_time)
        self.distance = haversine(self.src_lon, self.src_lat, self.dst_lon, self.dst_lat)
        self.end_time = self.start_time + self.interval_time
        self.estimated = distance2time(self.distance)


@dataclass
class Pro:
    id: str = field(default_factory=generate_id_pro)

    pre_lon: float = field(default_factory=generate_lon)
    pre_lat: float = field(default_factory=generate_lat)

    max_cap: int = field(default_factory=generate_capacity)
    cur_cap: int = field(default=0)

    completed: list = field(default_factory=list)

    waited_time: int = field(default=0)
    elapsed_time: int = field(default=0)
    extra_time: int = field(default=0)
    distance: float = field(default=0)


def main() -> None:
    df_delivery = pd.DataFrame.from_dict([Delivery() for _ in range(Config.num_delivery)])
    df_pro = pd.DataFrame.from_dict([Pro() for _ in range(Config.num_pro)])
    # visualize(df_delivery, df_pro)
    model = Model(df_delivery, df_pro)
    model.run()

if __name__ == '__main__':
    main()
