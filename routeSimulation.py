import math

# Haversine Formula To calculate distance between GPS points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Bin Locations
locations = {
    "HQ": (-6.1754, 106.8272), # Monas
    "Bin_1": (-6.1950, 106.8230), # Bundaran HI
    "Bin_2": (-6.1805, 106.8284), # Bank Indonesia
    "Bin_3": (-6.2000, 106.8167), # Somewhere nearby
    "Bin_4": (-6.2200, 106.8000), # Senayan
    "Bin_5": (-6.1600, 106.8300)  # Pasar Baru
}

# Scenario 1: Trash Collector visits every bins(without knowing which bin is full)
route_scenario_1 = ["HQ", "Bin_1", "Bin_2", "Bin_3", "Bin_4", "Bin_5", "HQ"]

total_distance_1 = 0
for i in range(len(route_scenario_1) - 1):
    p1 = locations[route_scenario_1[i]]
    p2 = locations[route_scenario_1[i+1]]
    total_distance_1 += haversine(p1[0], p1[1], p2[0], p2[1])

# 4. Scenario 2: Trash collector only visits the bins that are full, let's say in this case is bin 1 and bin 5
route_scenario_2 = ["HQ", "Bin_1", "Bin_5", "HQ"]

total_distance_2 = 0
for i in range(len(route_scenario_2) - 1):
    p1 = locations[route_scenario_2[i]]
    p2 = locations[route_scenario_2[i+1]]
    total_distance_2 += haversine(p1[0], p1[1], p2[0], p2[1])

print("--- ROUTE OPTIMIZATION SIMULATION ---")
print(f"Total Distance for scenario 1: {total_distance_1:.2f} km")
print(f"Total Distance for scenario 2: {total_distance_2:.2f} km")
print(f"Efficiency percentage: {((total_distance_1 - total_distance_2)/total_distance_1 * 100):.2f}%")