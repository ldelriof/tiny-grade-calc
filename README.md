# Route Distance Analysis Tool

This tool analyzes GPX files to calculate and visualize route distances, elevations, and gradients.

## Prerequisites

- Python 3.x
- Required packages:
  - gpxpy
  - pandas
  - geopy
  - matplotlib
  - statistics

Install dependencies:
```bash
pip install gpxpy pandas geopy matplotlib
```

## Usage

The script accepts GPX files and produces distance/elevation analysis with gradient visualization.

```bash
python dist_route.py [-f FILE] [-g {both,positive,negative}]
```

### Arguments

- `-f, --file`: Input GPX file name (without extension) from the data directory
  - Default: "cat_cross"
  - Example: `-f my_route`

- `-g, --grade`: Gradient type to visualize
  - Options: both, positive, negative
  - Default: "both"
  - Example: `-g positive`

### Example Commands

```bash
# Analyze default file with all gradients
python dist_route.py

# Analyze specific file with positive gradients only
python dist_route.py -f my_route -g positive
```

## Output

The script generates:
1. CSV report in `reports/{filename}_dist_report.csv`
2. JSON summary in `reports/{filename}_dist_report.json`
3. Interactive plot showing:
   - Elevation profile
   - Gradient visualization with color coding:
     - <6% : Green
     - 6-8% : Yellow
     - 8-10% : Orange
     - 10-13% : Red
     - >13% : Black
