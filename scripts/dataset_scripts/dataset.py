class DataSet:
    
    '''
    Parent Class for all supported datasets (i.e. ATL03, ATL07, MODIS, etc.)
    all sub classes must support the following methods for use in 
    colocated data class
    '''
    
    def __init__(self, boundingbox, timeframe):
        self.bounding_box = boundingbox
        self.time_frame = timeframe
        pass
    
    def visualize(self):
        pass
    
    def download(self, out_path):
        pass
    
    def get_meltpond_frcation(self):
        pass
    
    def get_sea_ice_fraction(self):
        pass
    
    def get_roughness(self):
        pass
    
    
