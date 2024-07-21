import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def selection_node(data: pd.DataFrame):
    """
    Function that allows the user to select nodes from a geographical map.
    The user can click on the nodes to select them. The selected nodes will
    be highlighted in red.

    :param data: Pandas DataFrame with the nodes data preprocessed.
    :return: list with the selected nodes tags.
    """
    # Create a scatter plot with the nodes.
    fig, ax = plt.subplots()
    sc = ax.scatter(data['longitude'], data['latitude'], c='YellowGreen', s=75)

    # Create a list to store the selected nodes.
    selected_nodes = []

    # Create a function to handle the click event on the plot.
    def on_click(event):
        """
        Function that handles the click event on the plot.
        :param event: Click event.
        :return: None
        """
        # Indentify the nearest node to the click event
        ind = sc.contains(event)[1]["ind"]
        if len(ind):
            node_index = ind[0]
            node = data.iloc[node_index]['tag']
            # Check if the node is already selected
            if node in selected_nodes:
                selected_nodes.remove(node)
                # Change color to indicate deselection
                sc.set_facecolor(['YellowGreen' if data.iloc[i]['tag'] not in selected_nodes else 'IndianRed' for i in range(len(data))])
            else:
                selected_nodes.append(node)
                # Change color to indicate selection
                sc.set_facecolor(['YellowGreen' if data.iloc[i]['tag'] not in selected_nodes else 'IndianRed' for i in range(len(data))])
            # Update the plot
            plt.draw()

    # Connect the click event to the plot
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Display the plot with the nodes
    plt.xlabel('Longitude [°]')
    plt.ylabel('Latitude [°]')
    plt.title('Node Selection')
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.15)
    plt.grid(which='minor', linestyle='-', linewidth='0.5', color='black', alpha=0.10)
    plt.show(block=True)

    # Print the selected nodes tag and number
    print("Number of selected nodes:", len(selected_nodes))
    print("Selected nodes:", selected_nodes)

    return selected_nodes


def plot_histograms(data: pd.DataFrame, relative: bool = True):
    """
    Function that plots histograms for a given data set.

    :param relative: Indicates if the histograms should be plotted as relative values.
    :param data: Dataframe with the data to generate the histograms.
    :return: Plot of the histograms.
    """
    if relative is True:
        fig, ax = plt.subplots()
        # Plot as a graph bar the histograms for each node
        for node in data.columns:
            ax.hist(data.index, bins=data.index, weights=data[node], alpha=0.7, label=node)
        ax.legend()
        plt.xlabel('Velocity [m/s]')
        plt.ylabel('Relative Frequency')
        plt.title('Velocity Histograms')
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.15)
        plt.grid(which='minor', linestyle='-', linewidth='0.5', color='black', alpha=0.10)
        plt.show(block=True)
    else:
        fig, ax = plt.subplots()
        # Plot as a graph bar the histograms for each node
        for node in data.columns:
            ax.bar(data.index, data[node], alpha=0.7, label=node)
        ax.legend()
        plt.xlabel('Velocity [m/s]')
        plt.ylabel('Number of records')
        plt.title('Velocity Histograms')
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.15)
        plt.grid(which='minor', linestyle='-', linewidth='0.5', color='black', alpha=0.10)
        plt.show(block=True)


def plot_power_curves_performance(cumulated_power: np.array):
    """
    Function that plots the cumulative power performance for the power curves.
    :param cumulated_power: cumulative power performance for the power curves.
    :return: bar plot with the cumulative power performance for each power curve.
    """
    x = np.arange(1, len(cumulated_power) + 1, 1)
    y = cumulated_power

    # Bar plot of the cumulative power performance curve. Maximum power is highlighted in red.
    fig, ax = plt.subplots()
    ax.bar(x, y, color='YellowGreen')
    ax.bar(np.argmax(y) + 1, y[np.argmax(y)], color='IndianRed')
    plt.xlabel('Power Curve')
    plt.ylabel('Cumulative Power [W]')
    plt.title('Cumulative Power Performance')
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.15)
    plt.grid(which='minor', linestyle='-', linewidth='0.5', color='black', alpha=0.10)
    plt.show(block=True)
    return
