import datetime

class colocateddata:
    
    def __init__(self, boundingbox, time_start, time_end):
        '''
        boundingbox: [lat1, lon1, lat2, lon2]
        time_start: datetime object
        time_end: datetime object
        '''
        self.bounding_box = boundingbox
        self.time_frame = timeframe
    
    
class IceSat2(colocateddata):
    def __init__(self):
        pass