from experiment_util import *

INSTANCE = "./Instances/A-n33-k6.vrp"
OUTPUT_FOLDER = "./output/"
SUBFOLDER = "activation_cost/"
suffix = "r-"
radius_vals = [10, 20, 25, 30, 35, 40]
angel_demand_vals = [i for i in range(30,61,5)]
activation_cost_vals = [w for w in range(10,51,10)]
connectivity_vals = [1, 0.9, 0.75, 0.6, 0.4]

# run(OUTPUT_FOLDER+SUBFOLDER, 
#     Network("./Instances/A-n33-k6.vrp",
#             num_angels=3,
#             radius=[20, 30, 25],
#             aid=16,
#             angel_locs=[(45,55), (70,70), (10,10)],
#             angel_demand=40),
#     "u1")

# run(OUTPUT_FOLDER+SUBFOLDER, 
#     Network("./Instances/P-n55-k15.vrp",
#             num_angels=3,
#             radius=20,
#             aid=22,
#             angel_locs=[(20,30), (20,60), (60,40)],
#             angel_demand=50),
#     "u2")

# run(OUTPUT_FOLDER+SUBFOLDER, 
#     Network("./Instances/P-n55-k15.vrp",
#             num_angels=3,
#             radius=20,
#             aid=19,
#             angel_locs=[(20,30), (20,60), (60,40)],
#             angel_demand=50),
#     "u3")

# clear_folder(OUTPUT_FOLDER+SUBFOLDER)
variable_radius(INSTANCE, OUTPUT_FOLDER+"radius/", suffix, radius_vals)
variable_angel_demand(INSTANCE, OUTPUT_FOLDER+"angel_demand/", suffix, angel_demand_vals)
variable_activation_cost(INSTANCE, OUTPUT_FOLDER+"activation_cost/", suffix, activation_cost_vals)
variable_connectivity(INSTANCE, OUTPUT_FOLDER+"connectivity/", suffix, connectivity_vals, 30)
# analyze_solutions(OUTPUT_FOLDER+SUBFOLDER)

# visualize_experiments(OUTPUT_FOLDER+SUBFOLDER, [f"w-{val}" for val in activation_cost_vals])