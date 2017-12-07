import rethinkdb as rdb
import time
import datetime
import numpy as np


##
## GLOBAL HELPERS
##
def logisticMap(x:float, alpha: (int, float)) -> float:
	return(1/(1 + np.e**(-alpha*x)))

def getReQLNow():
	timezone = time.strftime("%z")
	reql_tz = rdb.make_timezone(timezone[:3] + ":" + timezone[3:])
	now = datetime.datetime.now(reql_tz)
	return(now)