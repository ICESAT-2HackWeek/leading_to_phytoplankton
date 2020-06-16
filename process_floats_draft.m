%% Import ARGO synthetic floats

% Step 0: download full catalog of synthetic floats via: 
% wget -r -A Sprof.nc -nH --cut-dirs=4 ftp://ftp.ifremer.fr/ifremer/argo/dac/ -A Sprof.nc

% note that this is ~50Gb of data. 

% ---> kelsey bisson, dec 17, 2019
% ////////////////////////////////////////////////////////

% Step 1: Grab names of each file in the server with Sprof in name. 
% (stuff into a cell)

pipe='/data1/bisson/argo_coriolis_synth/Summer19/*/*/*Sprof*'
[e,r]=unix(['ls -1 ',pipe]);

% Step 1. Get nc files into workspace within cell structure
if (~e)
   r(end)=[];  % kill new line at end
   cellLs=eval([abs([123,39]),strrep(r,char(10),char([39,59,39])), ...
                abs([39,125])]); 
else
  warning(r)
  cellLs={};
end

% Step 2. Index where bbp700 is available (because we don't want to
% extract profiles where there isn't bbp).

% preallocate idxx
idxx = NaN(length(cellLs), 1); 

for i = 1: length(cellLs)
    try     
    ncid = netcdf.open(cellLs{i},'NOWRITE')
    varid = netcdf.inqVarID(ncid,'BBP700');
    idxx(i) = i;
    catch
    warning('No bbp in file, moving on...')
    idxx(i) = NaN;
    end
end

idxx(isnan(idxx))=[];

% Step 3. Loop over all cells and extract float profiles

for i = 1:length(idxx)
        
    ncid = netcdf.open(cellLs{idxx(i)},'NOWRITE')

    % Read in Pressure
    % note bad data is flagged with 99999
    varid = netcdf.inqVarID(ncid,'PRES');
    pres  = netcdf.getVar(ncid, varid,'double');
    pres(pres==99999)=NaN;
    
    % Read in Temp
    varid = netcdf.inqVarID(ncid,'TEMP');
    temp  = netcdf.getVar(ncid, varid,'double');
    temp(temp==99999)=NaN;
    
    % Read in Chl
    varid = netcdf.inqVarID(ncid,'CHLA');
    chl  = netcdf.getVar(ncid, varid,'double');
    chl(chl==99999)=NaN;
       
    % BBP 
    varid = netcdf.inqVarID(ncid,'BBP700'); 
    bbp   = netcdf.getVar(ncid, varid,'double');
    bbp(bbp==99999)=NaN;  

    % Read in practical salinity
    varid = netcdf.inqVarID(ncid,'PSAL');
    sal   = netcdf.getVar(ncid, varid,'double');
    sal(sal==99999)=NaN;  
     
    % Lat and Lon
    varid = netcdf.inqVarID(ncid,'LATITUDE');
    lat   = netcdf.getVar(ncid, varid,'double');
    varid = netcdf.inqVarID(ncid,'LONGITUDE');
    lon   = netcdf.getVar(ncid, varid,'double');

    % read in JULian day
    % days since 1950-01-01 00:00:00 UTC
    varid = netcdf.inqVarID(ncid,'JULD');
    juld   = netcdf.getVar(ncid, varid,'double');
        
% make lat lon juld day same size
newsz   = size(bbp,1) * size(bbp,2);
LAT     = reshape(repmat(lat',[size(bbp,1) 1]),[newsz 1]);
LON     = reshape(repmat(lon',[size(bbp,1) 1]),[newsz 1]);
JUD     = reshape(repmat(juld',[size(bbp,1) 1]),[newsz 1]);
Pres    = reshape(pres,[newsz 1]);
BBP     = reshape(bbp,[newsz 1]);
CHL     = reshape(chl,[newsz 1]);
TEMP    = reshape(temp,[newsz 1]);
SAL     = reshape(sal,[newsz 1]);
ID      = ones([newsz 1]);

% adjust days so theyre standalone and not w.r.t ref
time=datenum(JUD+datenum('01-Jan-1950')); 
date = datevec(time);

data = [LAT LON date(:,1:5) Pres BBP TEMP SAL CHL];

% throw out deep values and NaN pressure values
data(data(:,9)==99999,:)=NaN;
data(isnan(data(:,1)),:)=[];
data(isnan(data(:,9)),:)=[];

netcdf.close(ncid)

% stuff data into structure
alldata(i,1).floats = data;

clearvars -except alldata cellLs idxx

% keep track of progress
i
end

% collapse structure into 2d matrix with values
synth=cat(1, alldata.floats);

header= {'Lat','Lon','YYYY','MM','DD','HH','MM','sec','Pressure','BBP700(m^-1)',...
    'TEMP','SALINITY','CHL(ug/L)'};
save('/home/bissonk/floats/ARGO_synthetic_floats/BGCfloats_dec17.mat','synth','-v7.3');
