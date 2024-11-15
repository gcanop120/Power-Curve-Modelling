import numpy as np
import pandas as pd
from tqdm import tqdm


def get_histograms(data: pd.DataFrame, bin_size: float = 0.1, max_velocity: float = 2.8):
    """
    Function that generates histograms for a given data set.

    :param data: Dataframe with the data to generate the histograms.
    :param bin_size: Size of the bins for the histograms intervals.
    :param max_velocity: Maximum velocity value for the histograms.
    :return: Number of records in each bin for each node.
    """
    bins = np.arange(0, max_velocity + bin_size, bin_size)
    histograms = {}
    for node in data.columns:
        histograms[node] = np.histogram(data[node], bins=bins)[0]
    histograms = pd.DataFrame(histograms)
    histograms.index = bins[1:]
    return histograms


def get_frequency(histograms: pd.DataFrame):
    """
    Function that calculates the frequency of each bin for each node.

    :param histograms: Dataframe with the histograms.
    :return: Dataframe with the frequency of each bin for each node.
    """
    frequencies = histograms.div(histograms.sum(axis=0), axis=1)
    return frequencies


def gen_power_curves(frequencies: pd.DataFrame, min_ci_speed: float, min_rate_pct: float, delta_speed: float,
                     swept_area: float, cp: float = 0.37, water_density: float = 1025):
    """
    Function that generates power curves for a given data set.
    :param frequencies: Dataframe with the frequency of each bin for each node.
    :param min_ci_speed: Minimum cut-in speed for the water turbine in m/s.
    :param min_rate_pct: Minimum cut-in percentage based on the rated speed.
    :param delta_speed: Delta speed for the water turbine in m/s.
    :param swept_area: Swept area of the water turbine in m^2.
    :param cp: Maximum power coefficient for the water turbine.
    :param water_density: Density of the water in kg/m^3 (non-standard).
    :return: Minimum cut-in speed, maximum cut-out speed and power curves for each node.
    """
    # Compute the min cut in and max cut out speeds limits
    minimum_ci_vector = np.arange(min_ci_speed, (min_ci_speed * 4) + delta_speed, delta_speed)
    maximum_co_vector = minimum_ci_vector * (100 / min_rate_pct)
    maximum_co_vector = np.round(maximum_co_vector / delta_speed) * delta_speed

    velocities = list(frequencies.index)
    power_curves = []
    for i in range(len(minimum_ci_vector)):
        power_curve = []
        for velocity in velocities:
            if velocity < minimum_ci_vector[i]:
                power_curve.append(0)
            elif minimum_ci_vector[i] <= velocity < maximum_co_vector[i]:
                power_curve.append(0.5 * cp * swept_area * water_density * (velocity ** 3))
            else:
                power_curve.append(0.5 * cp * swept_area * water_density * (maximum_co_vector[i] ** 3))
        power_curves.append(power_curve)
    power_curves = np.array(power_curves).T
    return minimum_ci_vector, maximum_co_vector, power_curves


def cumulate_power_frequencies(frequency: pd.DataFrame, power_curves: np.array, hourly_data_points: int):
    """
    Function that cumulates the power generated by the water turbine for each power curve applied to each node.

    :param frequency: Dataframe with the frequency of each bin for each node.
    :param power_curves: Array with the power generated by the water turbine for each node.
    :param hourly_data_points: Number of hourly data points.
    :return: Cumulated power generated by the water turbine for each node.
    """

    cumulated_power = []
    frequency = frequency * hourly_data_points

    for curve in power_curves.T:
        power = 0
        for node in frequency.columns:
            power += np.sum(frequency[node] * curve)
        cumulated_power.append(power)
    cumulated_power = np.array(cumulated_power)
    return cumulated_power


def cumulate_power_time_series(min_rated_speed: float, max_rated_speed: float, filtered_nodes: pd.DataFrame, delta: float = 0.01,
                               density: float = 1025, swept_area: float = 0.7854, cp: float = 0.37):
    """
    Function that cumulates the power generated by the water turbine for each power curve applied to each node. The cumulative energy
    is computed for a time series data set instead of a frequency data set.
    :param min_rated_speed: Minimum rated speed for the water turbine in m/s.
    :param max_rated_speed: Maximum rated speed for the water turbine in m/s.
    :param filtered_nodes: Filtered time series data set.
    :param delta: Incremental value for the rated speed.
    :param density: Density of the water in kg/m^3 (non-standard).
    :param swept_area: Swept area of the water turbine in m^2.
    :param cp: Coefficient of performance for the water turbine.
    :return:
    """
    rated_speed_vector = np.arange(min_rated_speed, max_rated_speed + delta, delta)
    cumulated_power = []
    ideal_cumulated_power = []
    for rated_speed in tqdm(rated_speed_vector):
        power_per_node = []
        ideal_power_per_node = []
        for node in filtered_nodes.columns:
            power = 0
            ideal_power = 0
            for i in range(len(filtered_nodes)):
                if filtered_nodes[node][i] < (rated_speed * 0.3):
                    power += 0
                elif (rated_speed * 0.3) <= filtered_nodes[node][i] < rated_speed:
                    power += 0.5 * cp * swept_area * density * (filtered_nodes[node][i] ** 3)
                else:
                    power += 0.5 * cp * swept_area * density * (rated_speed ** 3)
                ideal_power += 0.5 * cp * swept_area * density * (rated_speed ** 3)
            power_per_node.append(power)
            ideal_power_per_node.append(ideal_power)
        cumulated_power.append(np.sum(power_per_node))
        ideal_cumulated_power.append(np.sum(ideal_power_per_node))
    cumulated_power = np.array(cumulated_power)
    ideal_cumulated_power = np.array(ideal_cumulated_power)
    capacity_factor = cumulated_power / ideal_cumulated_power
    return cumulated_power, capacity_factor


def optimal_rs_per_node(min_rated_speed: float, max_rated_speed: float, filtered_nodes: pd.DataFrame, delta: float = 0.01,
                        density: float = 1025, swept_area: float = 0.7854, cp: float = 0.37):
    """
    Function that computes the optimal rated speed for the power generation of each node.
    :param min_rated_speed: Minimum rated speed for the water turbine in m/s.
    :param max_rated_speed: Maximum rated speed for the water turbine in m/s.
    :param filtered_nodes: Pandas DataFrame with the filtered time series data.
    :param delta: Incremental value for the rated speed.
    :param density: Density of the water in kg/m^3 (non-standard).
    :param swept_area: Swept area of the water turbine in m^2.
    :param cp: Coefficient of performance for the water turbine.
    :return: optimal_rs: Array with the optimal rated speed for each node.
    """
    rated_speed_vector = np.arange(min_rated_speed, max_rated_speed + delta, delta)
    optimal_rs = []  # List with the optimal rated speed computed for each node. The length of the list is equal to the number of nodes.
    optimal_power = []  # List with the optimal power computed for each node. The length of the list is equal to the number of nodes.
    for node in tqdm(filtered_nodes.columns):
        power_per_rs = []
        for rated_speed in tqdm(rated_speed_vector):
            power = 0
            for i in range(len(filtered_nodes)):
                if filtered_nodes[node][i] < (rated_speed * 0.3):
                    power += 0
                elif (rated_speed * 0.3) <= filtered_nodes[node][i] < rated_speed:
                    power += 0.5 * cp * swept_area * density * (filtered_nodes[node][i] ** 3)
                else:
                    power += 0.5 * cp * swept_area * density * (rated_speed ** 3)
            power_per_rs.append(power)
        power_per_rs = np.array(power_per_rs)
        optimal_power.append(np.max(power_per_rs))
        optimal_rs.append(rated_speed_vector[np.argmax(power_per_rs)])

    return optimal_rs, optimal_power
