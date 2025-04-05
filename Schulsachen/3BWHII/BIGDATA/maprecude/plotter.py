import json
import sys
import matplotlib.pyplot as plt
import six

def simple_plot(data):
    years = sorted(data.keys())
    values = [data[year] for year in years]
    
    plt.figure(figsize=(12, 6))
    plt.plot(years, values, 'b-o')
    plt.title('Temperature Anomalies')
    plt.xlabel('Year')
    plt.ylabel('Anomaly (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as f:
                simple_plot(json.load(f))
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Usage: python plotter.py data.json")