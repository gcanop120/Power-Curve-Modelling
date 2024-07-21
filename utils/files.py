import pandas as pd


def load_time_series_geo(path: str, tag_id: str, latitude_id: str, longitude_id: str):
    """
    Function that loads a time series from a csv file. Reference file must have a header
    and three columns to be read: tag, latitude and longitude.

    :param path: Path to the csv file.
    :param tag_id: Column name for the tag.
    :param latitude_id: Column name for the latitude.
    :param longitude_id: Column name for the longitude.
    :return: A pandas DataFrame with the selected time series.
    """
    raw_data = pd.read_csv(path, header=0)
    selected_data = pd.DataFrame()
    selected_data['tag'] = raw_data[tag_id]
    selected_data['latitude'] = raw_data[latitude_id]
    selected_data['longitude'] = raw_data[longitude_id]

    return selected_data


def filter_time_series_data(path: str, index_id: str, nodes: list):
    """
    Function that filters a time series data based on the selected nodes.

    :param path: Path to the csv file with the time series data.
    :param index_id: ID name for the index column.
    :param nodes: List with the selected nodes from the geographical map.
    :return: filtered_data: A pandas DataFrame with the filtered time series data.
    """
    raw_data = pd.read_csv(path, header=0, index_col=index_id)
    raw_data.index = pd.to_datetime(raw_data.index)
    filtered_data = raw_data[nodes]
    return filtered_data
