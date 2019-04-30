import numpy as np
import pandas as pd
import sklearn
import random
from utils import *
from datetime import datetime

filename = './data.csv'
n = sum(1 for line in open(filename)) - 1  # Calculate number of rows in file
s = n // 1000  # sample size of 0.1%
skip = sorted(random.sample(range(1, n + 1), n - s))  # n+1 to compensate for header 
data = pd.read_csv(filename, skiprows=skip)

# select useful cols
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

timestamp_format = '%m/%d/%Y %I:%M:%S %p'

# fill missing Trip Seconds by subtracting timestamps
m = data[data['Trip Seconds'].isnull()].index.tolist()
print(f'missing values before diffing timestamps: {len(m)}')
for i in m:
    x = data['Trip Seconds'].iloc[i]
    y = data['Trip Start Timestamp'].iloc[i]
    z = data['Trip End Timestamp'].iloc[i]
    if (y and z):
        s = datetime.strptime(y, timestamp_format)
        e = datetime.strptime(z, timestamp_format)
        data.iloc[i, data.columns.get_loc('Trip Seconds')] = (e - s).total_seconds()

m2 = data[data['Trip Seconds'].isnull()].index.tolist()
print(f'missing values after diffing timestamps: {len(m2)}')
for i in m2:
    x = data['Trip Seconds'].iloc[i]
    y = data['Trip Start Timestamp'].iloc[i]
    z = data['Trip End Timestamp'].iloc[i]
    print(x, y, z)

# setting data types
data['Trip Minutes'] = (data['Trip Seconds'] / 60).astype('float16')
del data['Trip Seconds']
data['Trip Miles'] = data['Trip Miles'].astype('float16')     # no err on missing vals because NaN is float
data['Shared Trip Authorized'] = data['Shared Trip Authorized'].astype('bool')
data['Trips Pooled'] = data['Trips Pooled'].astype('uint8')

# monetary
data['Trip Total'] = data['Trip Total'].astype('float16')
data['Fare'] = data['Fare'].astype('float16')
data['Tip'] = data['Tip'].astype('float16')
data['Additional Charges'] = data['Additional Charges'].astype('float16')
data.round({
    'Trip Total': 2,
    'Fare': 2,
    'Tip': 2,
    'Additional Charges': 2
})

data['Pickup Community Area'] = data['Pickup Community Area'].fillna(-1).astype('category')
data['Dropoff Community Area'] = data['Dropoff Community Area'].fillna(-1).astype('category')

# decomposing timestamps
data = createTimestampCols(data, 'Trip Start Timestamp', timestamp_format)
data = createTimestampCols(data, 'Trip End Timestamp', timestamp_format)



print(data.describe())

# series of non-null rows in each col
# row_count = data.count()
# 21 rows

# .info() shows how many non-nulls
print(data.info(verbose=True))
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 17432011 entries, 0 to 17432010
Data columns (total 21 columns):
Trip ID                       object
Trip Start Timestamp          object
Trip End Timestamp            object
Trip Seconds                  float64
Trip Miles                    float64
Pickup Census Tract           float64
Dropoff Census Tract          float64
Pickup Community Area         float64
Dropoff Community Area        float64
Fare                          float64
Tip                           int64
Additional Charges            float64
Trip Total                    float64
Shared Trip Authorized        bool
Trips Pooled                  int64
Pickup Centroid Latitude      float64
Pickup Centroid Longitude     float64
Pickup Centroid Location      object
Dropoff Centroid Latitude     float64
Dropoff Centroid Longitude    float64
Dropoff Centroid Location     object
dtypes: bool(1), float64(13), int64(2), object(5)
memory usage: 2.6+ GB
None
'''

# describe shows more info
# append row for cols gte 70% non-null
# summary = data.describe()
# summary.loc['lt70PctNonNull'] = (summary.loc['count'] / row_count) < 0.7
# print(summary)
'''
                Trip Seconds    Trip Miles  Pickup Census Tract  ...  Pickup Centroid Longitude  Dropoff Centroid Latitude  Dropoff Centroid Longitude
count           1.742962e+07  1.743201e+07         1.228249e+07  ...               1.641080e+07               1.628047e+07                1.628047e+07
mean            1.070864e+03  5.932245e+00         1.703136e+10  ...              -8.766559e+01               4.189413e+01               -8.766793e+01
std             7.715778e+02  6.578893e+00         3.336269e+05  ...               5.958994e-02               6.048725e-02                6.399549e-02
min             0.000000e+00  0.000000e+00         1.703101e+10  ...              -8.791362e+01               4.165022e+01               -8.791362e+01
25%             5.320000e+02  1.800000e+00         1.703108e+10  ...              -8.767940e+01               4.187887e+01               -8.768103e+01
50%             8.630000e+02  3.600000e+00         1.703124e+10  ...              -8.765177e+01               4.189322e+01               -8.765177e+01
75%             1.389000e+03  7.400000e+00         1.703183e+10  ...              -8.763172e+01               4.192933e+01               -8.763186e+01
max             7.974000e+04  3.899000e+02         1.703198e+10  ...              -8.752995e+01               4.202122e+01               -8.752995e+01
lt70PctNonNull  0.000000e+00  0.000000e+00         0.000000e+00  ...               0.000000e+00               0.000000e+00                0.000000e+00
'''

# row_count_pct = row_count / num_rows
# row_count_pct_sub_70 = row_count_pct < 0.7
# print(row_count_pct)
# no cols are missing > 30%
'''
Trip ID                       False
Trip Start Timestamp          False
Trip End Timestamp            False
Trip Seconds                  False
Trip Miles                    False
Pickup Census Tract           False
Dropoff Census Tract          False
Pickup Community Area         False
Dropoff Community Area        False
Fare                          False
Tip                           False
Additional Charges            False
Trip Total                    False
Shared Trip Authorized        False
Trips Pooled                  False
Pickup Centroid Latitude      False
Pickup Centroid Longitude     False
Pickup Centroid Location      False
Dropoff Centroid Latitude     False
Dropoff Centroid Longitude    False
Dropoff Centroid Location     False
dtype: bool
'''


# print(data['Pickup Community Area'].value_counts())
'''
8.0     2935713
32.0    1543942
28.0    1534155
6.0     1175319
24.0    1119128
7.0      976432
22.0     664176
76.0     537933
3.0      380073
33.0     331215
77.0     248024
41.0     242706
5.0      215026
31.0     213740
56.0     202268
1.0      195686
21.0     194588
4.0      183953
16.0     171534
25.0     170364
2.0      143826
23.0     135244
43.0     122423
19.0     122415
35.0     110767
14.0     108888
15.0     108353
30.0     100982
29.0     100162
60.0      98039
         ...
40.0      45050
11.0      45046
17.0      44614
70.0      43644
65.0      42043
73.0      40161
13.0      39826
59.0      38897
46.0      38607
26.0      38580
57.0      32164
53.0      30758
75.0      29298
72.0      26118
62.0      24044
12.0      22607
64.0      22465
36.0      21591
48.0      20455
51.0      19313
45.0      18322
9.0       18312
18.0      17432
50.0      16003
74.0      15261
37.0      14824
54.0       8693
52.0       6933
47.0       5386
55.0       4667
Name: Pickup Community Area, Length: 77, dtype: int64
'''

# print(data['Pickup Census Tract'].value_counts())
'''
1.703184e+10    645087
1.703198e+10    444730
1.703132e+10    385940
1.703108e+10    367982
1.703183e+10    355658
1.703108e+10    341582
1.703108e+10    305975
1.703128e+10    240109
1.703108e+10    227706
1.703128e+10    224647
1.703133e+10    224421
1.703108e+10    180301
1.703132e+10    164233
1.703108e+10    158925
1.703108e+10    155008
1.703184e+10    148509
1.703183e+10    145154
1.703198e+10    143197
1.703108e+10    137181
1.703108e+10    128615
1.703184e+10    121506
1.703107e+10    113271
1.703132e+10    113088
1.703124e+10    111492
1.703184e+10    110775
1.703108e+10     97544
1.703108e+10     95226
1.703124e+10     89819
1.703184e+10     88831
1.703108e+10     87015
                 ...
'''