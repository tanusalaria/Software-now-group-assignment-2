import os
import csv
import math

DATA_FOLDER = "temperatures"

SEASON_AVG_FILE = "average_temp.txt"
TEMP_RANGE_FILE = "largest_temp_range_station.txt"
STABILITY_FILE = "temperature_stability_stations.txt"

SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

def read_all_files():
    station_data = {}   # {station: [temps]}
    seasonal_data = {s: [] for s in SEASONS}  # for global seasonal avg

    for file in os.listdir(DATA_FOLDER):
        if not file.endswith(".csv"):
            continue
        year = int(file.split("_")[-1].replace(".csv",""))
        path = os.path.join(DATA_FOLDER, file)
        with open(path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                station = row["STATION_NAME"].strip()
                if station not in station_data:
                    station_data[station] = []
                for month in MONTHS:
                    val = row[month].strip()
                    if val == "" or val.upper() == "NAN":
                        continue
                    temp = float(val)
                    station_data[station].append(temp)

                    # also add to seasonal pool
                    for season, months in SEASONS.items():
                        if month in months:
                            seasonal_data[season].append(temp)
    return station_data, seasonal_data

def seasonal_average(seasonal_data):
    with open(SEASON_AVG_FILE,"w") as f:
        for season in ["Summer","Autumn","Winter","Spring"]:
            temps = seasonal_data[season]
            if temps:
                avg = sum(temps)/len(temps)
                f.write(f"{season}: {avg:.1f}°C\n")
            else:
                f.write(f"{season}: No data\n")

def temperature_range(station_data):
    max_range = -1e9
    results = []
    for station, temps in station_data.items():
        if not temps: 
            continue
        tmax = max(temps)
        tmin = min(temps)
        trange = tmax - tmin
        if trange > max_range:
            max_range = trange
            results = [(station, trange, tmax, tmin)]
        elif abs(trange - max_range) < 1e-9:  # tie
            results.append((station, trange, tmax, tmin))

    with open(TEMP_RANGE_FILE,"w") as f:
        for station, trange, tmax, tmin in results:
            f.write(f"Station {station}: Range {trange:.1f}°C "
                    f"(Max: {tmax:.1f}°C, Min: {tmin:.1f}°C)\n")

def stddev(lst):
    if not lst:
        return float("nan")
    mean = sum(lst)/len(lst)
    variance = sum((x-mean)**2 for x in lst)/len(lst)
    return math.sqrt(variance)

def stability(station_data):
    stats = {}
    for station, temps in station_data.items():
        if temps:
            stats[station] = stddev(temps)

    if not stats:
        return

    min_std = min(stats.values())
    max_std = max(stats.values())
    most_stable = [s for s,v in stats.items() if abs(v-min_std)<1e-9]
    most_variable = [s for s,v in stats.items() if abs(v-max_std)<1e-9]

    with open(STABILITY_FILE,"w") as f:
        for s in most_stable:
            f.write(f"Most Stable: Station {s}: StdDev {stats[s]:.1f}°C\n")
        for s in most_variable:
            f.write(f"Most Variable: Station {s}: StdDev {stats[s]:.1f}°C\n")

def main():
    station_data, seasonal_data = read_all_files()
    seasonal_average(seasonal_data)
    temperature_range(station_data)
    stability(station_data)
    print("Analysis complete. Results saved to text files.")

if __name__ == "__main__":
    main()
