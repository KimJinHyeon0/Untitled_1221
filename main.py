from configs import Config
from utils import *


def main() -> None:
    delivery_list = [Delivery() for _ in range(Config.num_delivery)]
    pro_list = [Pro() for _ in range(Config.num_pro)]
    df_delivery = pd.DataFrame.from_dict(delivery_list)
    df_pro = pd.DataFrame.from_dict(pro_list)
    visualize(df_delivery, df_pro)


if __name__ == '__main__':
    main()