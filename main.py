import numpy as np
import pandas as pd
import sklearn

data = pd.read_csv('./data.csv')

# select desired features
data = data[[
    'Trip Start Timestamp',
    'Trip End Timestamp',
    'Trip Seconds',
    'Trip Miles',
    'Pickup Community Area',
    'Dropoff Community Area',
    'Fare',
    'Tip',
    'Additional Charges',
    'Trip Total',
    'Shared Trip Authorized',
    'Trips Pooled'
]]

print(data.describe().transpose())