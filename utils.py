import pyqtgraph as pg
import datetime
import time
from PyQt5.QtCore import QTime, QTimer



import pytz
UNIX_EPOCH_naive = datetime.datetime(1970, 1, 1, 0, 0) #offset-naive datetime
UNIX_EPOCH_offset_aware = datetime.datetime(1970, 1, 1, 0, 0, tzinfo = pytz.utc) #offset-aware datetime
UNIX_EPOCH = UNIX_EPOCH_naive

TS_MULT_us = 1e6

def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    return(int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult))

def int2dt(ts, ts_mult=TS_MULT_us):
    return(datetime.datetime.utcfromtimestamp(float(ts)/ts_mult))

def dt2int(dt, ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    delta = dt - epoch
    return(int(delta.total_seconds()*ts_mult))

def td2int(td, ts_mult=TS_MULT_us):
    return(int(td.total_seconds()*ts_mult))

def int2td(ts, ts_mult=TS_MULT_us):
    return(datetime.timedelta(seconds=float(ts)/ts_mult))

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
#        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]
         #return [int2dt(value).strftime("%H%M%S") for value in values]
         #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
         return [int2dt(value).strftime("%H:%M:%S") for value in values]

def timestamp():
 return int(time.mktime(datetime.datetime.now().timetuple()))

def now_timestamp():
 return int(time.time())

def int2dt(ts):
 if not ts:
     return datetime.datetime.utcfromtimestamp(ts) # workaround fromtimestamp bug (1)
 return(datetime.datetime.fromtimestamp(ts))
