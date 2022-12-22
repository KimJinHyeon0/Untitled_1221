class Config:
    num_delivery = 15
    num_pro = 3

    id_length_delivery = 5
    id_length_pro = 3

    # Delivery associated
    max_lat = 37.60
    min_lat = 37.45

    max_lon = 127.15
    min_lon = 126.85

    max_baggage = 20
    min_baggage = 5

    max_start_time = 1200  # 8pm
    min_start_time = 540  # 9am

    max_elapsed_time = 60  # minute
    min_elapsed_time = 20

    max_distance = 5000  # miter
    min_distance = 500

    max_pickup_time = 60  # minute
    min_pickup_time = 15

    # Pro associated
    max_capacity = 100
    min_capacity = 50

