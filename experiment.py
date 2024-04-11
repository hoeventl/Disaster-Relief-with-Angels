from experiment_util import *

INSTANCE = "./Instances/TH-n11-k2.vrp"
OUTPUT_FOLDER = "./output-simple/"
SUBFOLDER = "angel_demand/"
suffix = "r-"
radius_vals = [60, 75, 90, 105, 120]
angel_demand_vals = [i for i in range(25,36,1)]
activation_cost_vals = [w for w in range(70,91,5)]
connectivity_vals = [0.9, 0.75, 0.5]
connectivity_vals2 = [0.6, 0.45]

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

#################
# run(OUTPUT_FOLDER+"special/",
#     Network("./Instances/P-n55-k15.vrp",
#             num_angels=3,
#             radius=20,
#             aid=17,
#             angel_locs=[(20,30), (20,60), (60,40)],
#             angel_demand=50),
#     "P-n55")
# run(OUTPUT_FOLDER+"special/",
#     Network("./Instances/A-n37-k6.vrp",
#             num_angels=3,
#             radius=20,
#             aid=15,
#             angel_locs=[(10,40), (65,45), (90,90)],
#             angel_demand=50),
#     "A-n37")
# run(OUTPUT_FOLDER+"special/",
#     Network("./Instances/A-n80-k10.vrp",
#             num_angels=3,
#             radius=20,
#             aid=15,
#             angel_locs=[(35,65), (70,20), (75,75)],
#             angel_demand=50),
#     "A-n80")
# run(OUTPUT_FOLDER+"special/",
#     Network("./Instances/X-n101-k25.vrp",
#             num_angels=6,
#             radius=100,
#             aid=25,
#             angel_locs=[(800,800), (900,100), (200,200), (200,900), (600,700), (1000,500)],
#             angel_demand=50),
#     "X-n101")
# run(OUTPUT_FOLDER+"special/",
#     Network("./Instances/B-n44-k7.vrp",
#             num_angels=4,
#             radius=10,
#             aid=15,
#             angel_locs=[(40,50), (70,100), (100,50), (90,20)],
#             angel_demand=40),
#     "B-n44")

#clear_folder(OUTPUT_FOLDER+"activation_cost/")
#clear_folder(OUTPUT_FOLDER+"angel_demand/")
#clear_folder(OUTPUT_FOLDER+"connectivity/")
variable_radius(INSTANCE, OUTPUT_FOLDER+"radius/", "r-", radius_vals)
variable_angel_demand(INSTANCE, OUTPUT_FOLDER+"angel_demand/", "ad-", angel_demand_vals)
variable_activation_cost(INSTANCE, OUTPUT_FOLDER+"activation_cost/", "w-", activation_cost_vals)
variable_connectivity(INSTANCE, OUTPUT_FOLDER+"connectivity/", "c-", connectivity_vals, 5)
# analyze_solutions(OUTPUT_FOLDER+"connectivity/")

# visualize_experiments("output/"+"angel_demand/", ["r-60"])
