# The Reasonable Crowd Dataset

Welcome to the Reasonable Crowd dataset! This dataset will help you develop and test driving behavior specification models.

You can find the paper associated with the dataset at  [https://arxiv.org/abs/2107.13507](https://arxiv.org/abs/2107.13507).

## Data overview

Your first step will be to download the data from [here](https://reasonable-crowd-public-data.s3.amazonaws.com/reasonable_crowd_data.zip).

NOTES:
- Once unzipped, the data will expand to about 27.5 gb!
- The names of the realizations follow this convention: `X_#-l` where `X` is either `U` (for the urban environment) or `S` (for the suburban environment). `#` denotes the scenario number in each environment. `l` is a letter counting the realization in each scenario. For example, `U_7-b` means realization `b` in `scenario` 7 of the environment `U`.


### Videos
We place the videos annotators viewed in the `videos` directory.

### Annotations
We've constructed a website to explore annotations: [annotions explorer](https://reasonable-crowd-public-data.s3.amazonaws.com/annotations_explorer/index.html). 
Click on `videos are synced` to unsync or sync the videos' playback.

Moreover, the `annotations` folder contains detailed data on the annotations:
1. `workers.txt` is a list of the ids of the workers that annotated the dataset.
2. We share the annotations for each realization in both a `pickle` and a `json` format. Each are structured as follows:
   1.  `annotations.pickle` stores a `Dict[str, Dict[Tuple[str, str], List[str]]]` of the form `{scenario_id: {(realization_id1, realization_id2): [ids of workers that preferred realization_id1 over realization_id2]}}`
   2.   `annotations.json` has a scenario as a primary key followed by all the possible realization pairs in that scenario with the ids of workers that preferred one realization over another. For example, 
   ```json
    "U_7": {
    "U_7-a ;; U_7-b": ["w_45"],
    "U_7-c ;; U_7-b": [],
    "U_7-d ;; U_7-a": ["w_10", "w_31"],
    }
   ```
   means that for scenario `U-7`, the worker with id `w_45` preferred realization `U_7-a` over `U_7-b`. No workers preferred `U_7-c` over `U_7-b`. The workers with ids `w_10` and `w_31` preferred realization `U_7-d` over `U_7-a`.

NOTES: 
- Sometimes more than one worker annotates the same trajectory pair.

### Trajectories
For each realization, we share the trajectories of all agents in a json format. The json file is a list of states at different times. Each state has the following fields:
- `type`: whether it's ego, a vehicle or a pedestrian.
- `x_meters`: Agent's center's location's x-coordinate (in meters).
- `y_meters`: Agent's center's location's y-coordinate (in meters).
- `heading_radians`: Agent's heading / yaw in radians.
- `x_velocity_meters_per_second`: agent's velocity along the x-direction in meters per second.
- `y_velocity_meters_per_second`: agent's velocity along the y-direction in meters per second.
- `timestamp`: When the state was recorded while running the simulation (in microseconds).
- `id`: The agent's id. Each agent has a unique id so we can track them through time.
- `footprint`: a list of x, y coordinates in meters outlining the agent's profile. See the tutorial for how to use the `footprint`.

NOTES: 
- The pedestrian's footprint is approximated as a bounding box.
- Ego's state is recorded at a higher frequency than that of other agents.

### Maps

For each of the environments, `U` and `S`, we provide different map layers. We encode the maps in the `gpkg` format, which is widely used and has many tools associated with it (such as the `geopandas` pip pkg). 

For ease of use, we provide each map layer in a different file. For example, `U_intersections.gpkg` is the intersections map layer for the `U` environment.
The different map layers are:

#### Lane Polygons (`lanes_polygons`)
A polygonal representation of a lane

#### Lane group polygons (`lane_groups_polygons`)
A group of adjacent lanes that travel in the same direction

#### Intersections (`intersections`)
A polygonal representation of an intersection

#### Pedestrian crosswalks (`ped_crossings`)
A polygonal representation of a pedestrian crosswalk.
Note that for this layer, the field `is_marked` represents whether this crosswalk has actual road markings.

#### boundaries (`boundaries`)
Boundaries can come in different types. Specifically, `boundary_type` can be the following:
- `LaneDivider`: A left or right boundary of a given lane.
- `RoadDivider`: A left or right boundary of a lane group. Helps us know if we switched to driving on the wrong side of the road.
- `Roadside`:  Boundary between road and a curb/ pavement.
- `Virtual` means e.g. virtual lane boundaries in an intersection

#### Road (`road_segments`)
Polygonal representation of the road (excluding intersections).

## Tutorials
To get acquainted with the data, we created `tutorials/tutorial.ipynb`. We highly recommend that you go through it to become familiar with the data. 

Note that to run the tutorial you need the following pip pkgs: geopandas, matplotlib, numpy, imageio and shapely.