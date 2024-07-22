from utils.files import load_time_series_geo
from utils.files import filter_time_series_data
from utils.mapping import selection_node
from utils.mapping import plot_histograms
from utils.generation import get_histograms
from utils.generation import get_frequency
from utils.generation import gen_power_curves
from utils.generation import cumulate_power_frequencies
from utils.mapping import plot_power_curves_performance


if __name__ == '__main__':
    PATH_geo = "../resources/Time_Series_Statistical_Features_per_Node.csv"
    PATH_data = "../resources/Time_Series_Velocity_Data_per_Node.csv"

    data_geo = load_time_series_geo(path=PATH_geo, tag_id="Tag", latitude_id="Latitude", longitude_id="Longitude")
    selected_nodes = selection_node(data_geo)
    filtered_nodes = filter_time_series_data(path=PATH_data, index_id="Date", nodes=selected_nodes)
    histograms = get_histograms(filtered_nodes, bin_size=0.025, max_velocity=2.75)
    frequencies = get_frequency(histograms)
    plot_histograms(frequencies, relative=True)
    # Power curves return three values: minimum cut-in speed, maximum cut-out speed and power curves for each node.
    power_curves = gen_power_curves(frequencies=frequencies, min_ci_speed=0.2, min_rate_pct=30,
                                    delta_speed=0.025, swept_area=0.7854, cp=0.37, water_density=1025)
    cumulated_power = cumulate_power_frequencies(frequency=frequencies, power_curves=power_curves[2], hourly_data_points=len(filtered_nodes))
    plot_power_curves_performance(cumulated_power)

    """
    # Save frequencies data to a csv file
    pd.DataFrame(frequencies).to_csv("Frequencies_Performance.csv")
    # Save power_curves[2] data to a csv file
    pd.DataFrame(power_curves[2]).to_csv("Power_Curves_Performance.csv")
    """
