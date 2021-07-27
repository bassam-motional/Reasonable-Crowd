""" Script to visualize a realization """

import json
import os
from typing import Any, Dict

import imageio
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon


def dist_between_2_states(state1: Dict, state2: Dict) -> float:
    """
    Return the distance between 2 states
    """
    dx = state1["x_meters"] - state2["x_meters"]
    dy = state1["y_meters"] - state2["y_meters"]

    return np.sqrt(dx ** 2 + dy ** 2)


def visualize_realization(
    traj_path: os.path,
    map_path: os.path,
    save_dir: os.path,
    dist_threshold_from_ego: float = 30,
    dt_refresh_fig: float = 0.25,
) -> None:
    """
    A demo function showing how to use the plotting functions
    :param traj_path: Path of trajectory to update.
    :param map_path: Path to map file
    :param save_dir: Where to save the plots.
    :param dist_threshold_from_ego: If an agent's distance to ego is greater than this threshold,
        then the agent is not plotted. Units: Meters.
    :param dt_refresh_fig: how often to refresh the figure and create a new one. Units: seconds.
    """
    with open(traj_path, "r") as j_file:
        traj_states = json.load(j_file)
    map_df = gpd.read_file(map_path)

    save_dir = os.path.join(save_dir, os.path.basename(traj_path.split(".")[0]))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Plotting parameters
    ego_color = "black"
    ped_color, veh_color = "red", "blue"

    n_states = len(traj_states)
    ind = 0
    curr_ego = traj_states[0]
    figs = []  # keep track of figs to make into a movie
    fig = None
    # keep track of which objects have been plotted: want to plot each obj at most once per fig
    plotted_obj_ids = set()
    # make greater than dt to trigger condition below in while loop
    time_elapsed_since_fig_created = 2 * dt_refresh_fig
    # from above while loop we are guarranteed that curr state is ego
    while ind < n_states:
        state = traj_states[ind]
        time_elapsed = state["timestamp"] / 1e6  # in seconds

        if time_elapsed_since_fig_created > dt_refresh_fig:
            if fig is not None:
                plt.savefig(os.path.join(save_dir, f"{ind}.png"))
                plt.close(fig)

            # create a new figure
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.axis("off")

            map_df.plot(ax=ax)

            # update relevant variables
            # index of object when figure created
            ind_obj_fig_created = ind
            time_elapsed_since_fig_created = 0
            plotted_obj_ids = set()

            ax.set_title(f"Time elapsed: {time_elapsed: .2f} seconds")

            # center around ego
            fig_half_range = 0.7 * dist_threshold_from_ego
            ego_x, ego_y = curr_ego["x_meters"], curr_ego["y_meters"]
            xlimits = [ego_x - fig_half_range, ego_x + fig_half_range]
            ylimits = [ego_y - fig_half_range, ego_y + fig_half_range]
            ax.set_xlim(xlimits), ax.set_ylim(ylimits)

            ax.set_aspect("equal")

        if state["type"] == "vehicle":
            color = veh_color
        elif state["type"] == "pedestrian":
            color = ped_color
        elif state["type"] == "ego":
            curr_ego = state
            color = ego_color

        if dist_between_2_states(curr_ego, state) > dist_threshold_from_ego:
            ind += 1
            continue

        if state["id"] not in plotted_obj_ids:
            plotted_obj_ids.add(state["id"])
            footprint = Polygon(state["footprint"])
            ax.plot(*footprint.exterior.xy, color=color)

        ind += 1

        # update time since we created a figure
        time_elapsed_since_fig_created = (
            state["timestamp"] - traj_states[ind_obj_fig_created]["timestamp"]
        ) / 1e6

    plt.close("all")

    # convert to video
    images = []
    sorted_filenames = []
    for filename in os.listdir(save_dir):
        sorted_filenames.append(int(filename.split(".")[0]))
    sorted_filenames.sort()
    sorted_filenames = [os.path.join(save_dir, f"{f}.png") for f in sorted_filenames]
    for filename in sorted_filenames:
        images.append(imageio.imread(os.path.join(save_dir, filename)))
    imageio.mimsave(os.path.join(save_dir, "movie.mp4"), images, fps=1 / dt_refresh_fig)


if __name__ == "__main__":
    map_path = (
        "/home/bhelou/Documents/data/rc_cleaning/data_share/maps/U_boundaries.gpkg"
    )
    trajectory_path = (
        "/home/bhelou/Documents/data/rc_cleaning/data_share/trajectories/U_27-a.json"
    )

    # map_path = (
    #     "/home/bhelou/Documents/data/rc_cleaning/data_share/maps/S_boundaries.gpkg"
    # )
    # trajectory_path = (
    #     "/home/bhelou/Documents/data/rc_cleaning/data_share/trajectories/S_23-a.json"
    # )

    save_dir = "/home/bhelou/Documents/data/rc_cleaning/data_share/plots_CAN_DELETE"

    visualize_realization(trajectory_path, map_path, save_dir)
