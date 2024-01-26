
import pandas as pd

from pathlib import Path

dir_path = Path(__file__).parent.resolve()
print('created path')
data = pd.read_csv(dir_path / 'sensor_timeseries.csv')

print(data.mean())
