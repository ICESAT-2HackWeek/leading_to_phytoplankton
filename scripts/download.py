def download(bbox, timeframe, beam, earthdata_uid, email): 
    
    import os
    from icepyx import icesat2data as ipd
    from icepyx import core
    import readers as rd
    
    short_name = ATL03 '''fill in with name of whichever DataSet this is a member function of'''
    
    region.ipd.Icesat2Data(short_name, bbox, timeframe)
    region.avail_granules()
    
    print(region.avail_granules())
    if ('y' or 'yes' == input("Here's what we've got! Continue? (y/n)")):
        region.earthdata_login()
        
        path = './download/' + short_name
        region.download_granules(path)
        files = region.avail_granules(ids=True)
        
        print("Downloaded! Have a great day!")
    else:
        print("Nothing was downloaded")
        exit()

    
    for file in files:
        f = h5py.File(path+file, 'r')
        df = rd.getATL03(f,beam)
        
        #trim to bounding box
        df_cut=df[bbox]
        
        #convert time to UTC
        epoch=f['/ancillary_data/atlas_sdp_gps_epoch'][0]
        df_cut['time']=Time(epoch+df_cut['dt'],format='gps').utc.datetime
        
        #caculate along track distance
        df_cut['AT_dist']=df_cut.x-df_cut.x.values[0]
        
        #save a dictionary entry in the DataSet
        self{file} = df_cut
        
        