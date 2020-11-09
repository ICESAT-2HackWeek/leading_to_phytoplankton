from .dataset_scripts import *
import matplotlib.pyplot as plt

from .dataset_scripts.atl07 import ATL07


class Colocateddata:
    
    def __init__(self, boundingbox, time_start, time_end, proj='Default'):
        '''
        boundingbox: [lon1, lon2, lat1, lat2]
        time_start: datetime object
        time_end: datetime object
        projection: a string name of projection to be used for plotting (e.g. 'Mercator', 'NorthPolarStereographic')
        '''
        self.bounding_box = boundingbox
        self.time_frame = [time_start, time_end]
        self.datasets = {}
        self.projection = self._determine_proj(proj)

    def _determine_proj(self, proj):
        if proj == 'Default':
            # based on the bounding box specified, determine an appropriate projection
            if min(self.bounding_box[2], self.bounding_box[3]) > 30:
                return 'NorthPolarStereographic'
            elif proj == 'NorthPolarStereo':
                pass
                # todo: check other regions for most appropriate proj
                #  ...

        else:
            # todo: check that user entered valid proj name
            return proj

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
        
    def show_area_overlap(self, show_datasets=None, porj='NorthPolarStereo'):
        ds2plot = []
        if show_datasets:
            ds2plot = show_datasets
        else:
            ds2plot = self.datasets

        # settings for plots that are common to all figures
        # ...

        plt.figure(figsize=(8, 8), dpi=600)
        if self.projection == 'NorthPolarStereographic':
            ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0))  # choose polar sterographic for projection
        elif self.projection == 'Mercator':
            ax = plt.axes(projection=ccrs.Mercator(central_longitude=0))  # choose polar sterographic for projection

        ax.coastlines(resolution='50m', color='black', linewidth=1)

        for i in ds2plot:
            # call individual plot functions from each dataset object
            pass


        print('This will show all of the data overlapping on the same axes')
        pass
    
    def init_dataset(self, dataset_list):
        
        for i in dataset_list:
            print('Searching though {0}'.format(i))
            self._add_dataset(i)
        
        print('search complete')
    
    
    
    def _add_dataset(self, dataset_name):
        '''
        Adds dataset objcet to dataset dictionary
        '''
        
        if dataset_name == 'ATL03':
            self.datasets[dataset_name] = ATL03(self.bounding_box, self.time_frame)
        elif dataset_name == 'ATL07':
            self.datasets[dataset_name] = ATL07(self.bounding_box, self.time_frame)
        else:
            print('Error: {0} is not a supported dataset'.format(dataset_name))
            print('Permitted datasets are \n\tATL03, ATL07')
    
    
    



# dat = Colocateddata([1,2,3,4], yesterday, today)
# dat.init_dataset([ATL03])