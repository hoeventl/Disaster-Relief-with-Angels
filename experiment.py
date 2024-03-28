from experiment_util import *

INSTANCE = "./Instances/TH-n11-k2.vrp"
OUTPUT_FOLDER = "./output/"
SUBFOLDER = "miscellaneous/"
suffix = "r-"
radius_vals = [0, 60, 70, 95, 105, 125]
angel_demand_vals = [i for i in range(10,51,5)]
activation_cost_vals = [w for w in range(10,91,10)]
connectivity_vals = [1, 0.9, 0.75, 0.5, 0.3]

run(OUTPUT_FOLDER+SUBFOLDER, 
    Network("./Instances/A-n33-k6.vrp",
            num_angels=3,
            radius=[20, 30, 25],
            aid=16,
            angel_locs=[(45,55), (70,70), (10,10)],
            angel_demand=40),
    "u1")


# clear_folder(OUTPUT_FOLDER+SUBFOLDER)
# variable_radius(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, radius_vals)
# variable_angel_demand(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, angel_demand_vals)
# variable_activation_cost(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, activation_cost_vals)
# variable_connectivity(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, connectivity_vals, 10)
analyze_solutions(OUTPUT_FOLDER+SUBFOLDER)

visualize_experiments(OUTPUT_FOLDER+SUBFOLDER, ["u1"])