from datetime import datetime
from constants import *

def mapCommunityCodeToName(code):
    return CHICAGO_COMMUNITY_AREA_CODE_TO_NAME[code]

def decomposeTimestamps(format):
    '''pass df or series with datetime values
    '''
    def _decompose(datetimeStr):
        d = datetime.strptime(datetimeStr, format)
        return d.hour, d.weekday(), d.day, d.month
    return _decompose

def createTimestampCols(df, col_name, format):
    hour = col_name.replace('Timestamp', 'Hour')
    weekday = col_name.replace('Timestamp', 'Weekday')
    day = col_name.replace('Timestamp', 'Day')
    month = col_name.replace('Timestamp', 'Month')
    df[hour], df[weekday], df[day], df[month] = zip(*df[col_name].map(decomposeTimestamps(format)))
    del df[col_name]
    df[hour] = df[hour].astype('category')
    df[weekday] = df[weekday].astype('category')
    df[day] = df[day].astype('category')
    df[month] = df[month].astype('category')
    return df