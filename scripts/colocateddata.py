from dataset_scripts import *


class Colocateddata:
    
    def __init__(self, boundingbox, time_start, time_end):
        '''
        boundingbox: [lat1, lon1, lat2, lon2]
        time_start: datetime object
        time_end: datetime object
        '''
        self.bounding_box = boundingbox
        self.time_frame = [time_start, time_end]
        self.datasets = {}
    
    def __str__(self):
        '''
        Returns a string representation of self
        '''
        
        str = 'bounding box: {0}\nStart time: {1}\nEnd time: {2}\nDatasets:'.format(
            self.bounding_box, self.time_frame[0], self.time_frame[1])
        
        if not self.datasets:
            str += ' No datasets have been added yet'
        else:
            for i in self.datasets.keys():
                str += '\n\t' + i
        
        return str
        
    def show_area_overlap(self):
        pass
    
    def init_dataset(self, dataset_list):
        
        for i in dataset_list:
            print('Searching though {0}'.format(i))
            self._add_dataset(i)
        
        print('search complete')
    
    
    
    def _add_dataset(self, dataset_name):
        
        if dataset_name == 'ATL03':
            self.datasets[dataset_name] = ATL03(self.bounding_box, self.time_frame)
            print('ATL03')
        elif dataset_name == 'ATL07':
            print('ATL07')
        else:
            print('Error: {0} is not a supported dataset'.format(dataset_name))
            print('Permitted datasets are \n\tATL03, ATL07')
    
    
    

