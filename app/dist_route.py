import gpxpy
import pandas as pd
import geopy.distance
import statistics
from matplotlib import pyplot
from argparse import ArgumentParser

grade_types = ["both", "positive", "negative"]

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file", default="cat_cross")
parser.add_argument("-g", "--grade", dest="grade", default="both", choices=grade_types)

args = parser.parse_args()
print(args)
file = args.file

gpx_file = open(f"data/{file}.gpx", "r")
gpx = gpxpy.parse(gpx_file)

points = []
eles = []
distance = 0
cum_distance = 0
tot_dist = 0
seg_dist = 50
point2 = None
p_ele = None
for track in gpx.tracks:
    for segment in track.segments:
        for p in segment.points:
            point1 = (p.latitude, p.longitude)
            if not point2:
                point2 = point1

            p_distance = geopy.distance.distance(point1, point2).m
            point2 = point1

            distance += p_distance
            cum_distance += p_distance / 1000
            assert p.elevation is not None
            eles.append(p.elevation)

            tot_dist += distance * 300000000

            if distance >= seg_dist:
                elev = statistics.median(eles)
                if not p_ele:
                    p_ele = elev

                gradient = (elev - p_ele) / distance if distance > 0 else 0

                points.append(
                    {
                        "time": tot_dist,
                        "latitude": p.latitude,
                        "longitude": p.longitude,
                        "distance": distance,
                        "cum_distance": cum_distance,
                        "elevation": elev,
                        "gradient": gradient * 100,
                        "tot_points": len(eles),
                    }
                )
                distance = 0
                eles = []
                p_ele = elev


df = pd.DataFrame.from_records(points)
df.set_index("cum_distance", inplace=True)

print(df.loc[df.gradient > 0])

print(df.mean())

df.to_csv(f"reports/{file}_dist_report.csv")
df.loc[df.index < 3].to_json(
    f"reports/{file}_dist_report.json", orient="records", indent=4
)

ax = df["elevation"].plot()

ys = df.elevation

match args.grade:
    case "both":
        ysi = abs(df.gradient)
    case "positive":
        ysi = df.gradient
    case "negative":
        ysi = -df.gradient

gradients = {0: "#6f6", 2: "#cfc", 5: "yellow", 8: "orange", 10: "red", 13: "black"}

for g, color in gradients.items():
    kwargs = {"where": None, "color": color}
    if g > 0:
        kwargs["where"] = ysi >= g

    ax.fill_between(
        x=df.index, y1=ys, interpolate=True, label=f"Gradient < {g}%", **kwargs
    )

ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), ncol=7)

pyplot.show()
