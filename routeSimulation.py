import math

# 1. Define the Haversine Formula (To calculate distance between GPS points)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 2. Define 5 Locations (Example: Around Monas/Jakarta)
locations = {
    "Depot": (-6.1754, 106.8272), # Monas
    "Bin_A": (-6.1950, 106.8230), # Bundaran HI
    "Bin_B": (-6.1805, 106.8284), # Bank Indonesia
    "Bin_C": (-6.2000, 106.8167), # Somewhere nearby
    "Bin_D": (-6.2200, 106.8000), # Senayan
    "Bin_E": (-6.1600, 106.8300)  # Pasar Baru
}

# 3. Scenario 1: Traditional Route (Visit EVERY Bin)
# Route: Depot -> A -> B -> C -> D -> E -> Depot
route_all = ["Depot", "Bin_A", "Bin_B", "Bin_C", "Bin_D", "Bin_E", "Depot"]

dist_all = 0
for i in range(len(route_all) - 1):
    p1 = locations[route_all[i]]
    p2 = locations[route_all[i+1]]
    dist_all += haversine(p1[0], p1[1], p2[0], p2[1])

# 4. Scenario 2: Smart Route (Only Full Bins)
# Let's say only Bin A and Bin E are full
route_smart = ["Depot", "Bin_A", "Bin_E", "Depot"]

dist_smart = 0
for i in range(len(route_smart) - 1):
    p1 = locations[route_smart[i]]
    p2 = locations[route_smart[i+1]]
    dist_smart += haversine(p1[0], p1[1], p2[0], p2[1])

# 5. Print Results
print("--- ROUTE OPTIMIZATION SIMULATION ---")
print(f"Scenario 1 (Traditional): {dist_all:.2f} km")
print(f"Scenario 2 (Smart System): {dist_smart:.2f} km")
print(f"Efficiency Savings: {((dist_all - dist_smart)/dist_all * 100):.2f}%")