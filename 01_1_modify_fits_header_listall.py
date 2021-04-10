# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 01:00:19 2018
@author: user

"""

from datetime import datetime
from astropy.io import fits
import astro_utilities

add_log = True
if add_log == True :
    log_file = 'astro_Python.log'
    err_log_file = 'astro_Python_err.log'

master_file_dir_name = 'master_file_Python/'
processing_dir_name = 'processing_Python/'
integration_dir_name = 'integration_Python/'
alignment_dir_name = 'alignment_Python/'

c_method = 'median'    

base_dir = "../CCD_new_files"

fullnames = astro_utilities.getFullnameListOfallFiles(base_dir)
print ("fullnames: {}".format(fullnames))
    
for fullname in fullnames[:] :
#fullname = fullnames[0]
    if fullname[-4:] == ".fit" :
        print('#'*60)
        print('Starting......\n{0} ...'.format(fullname))
        fullname_el = fullname.split('/')
        foldername_el = fullname_el[-2].split('_')
        optic_name = foldername_el[-4]
        #../
        #NEW-fits/
        #FSQ106-x0.73/
        #-_Dark_-_-_-_-_STF-8300M_-_1x1bin/
        #-_Dark_-_2020-03-25_120sec_-_STF-8300M_-_1x1bin/
        #-_Dark_-_2020-03-25-12-35-58_120sec_FSQ106-x0.73_STF-8300M_-19C_1x1bin.fit
    
        try :
            with fits.open('{0}'.format(fullname), mode="append") as hdul :
                if not 'OPTIC' in hdul[0].header :
                    hdul[0].header.append('OPTIC', 
                                       '{0}'.format(optic_name), 
                                       'OPTIC information')
                    astro_utilities.write_log(log_file, 
                        '{1} ::: OPTIC information is appended at {0}...'\
                        .format(fullname, datetime.now()))
            with fits.open('{0}'.format(fullname), mode="update") as hdul :
                # Change something in hdul.
                if not hdul[0].header['OPTIC'] : 
                    hdul[0].header['OPTIC'] = '{0}'.format(optic_name)
                    astro_utilities.write_log(log_file, 
                        '{1} ::: OPTIC information is modified at {0}...'\
                        .format(fullname, datetime.now()))
                elif not '{0}'.format(optic_name).lower() in hdul[0].header['OPTIC'].lower() : 
                    hdul[0].header['OPTIC'] = '{0}'.format(optic_name)
                    astro_utilities.write_log(log_file, 
                        '{1} ::: OPTIC information is modified at {0}...'\
                        .format(fullname, datetime.now()))
                else : 
                    hdul[0].header['OPTIC'] = '{0}'.format(optic_name)
                    astro_utilities.write_log(log_file, 
                        '{1} ::: OPTIC information is modified at {0}...'\
                        .format(fullname, datetime.now()))
                hdul[0].header.append('COMMENT', 
                                       'add HEADER OPTIC {0}'.format(optic_name), 
                                       'add HEADER OPTIC {0}'.format(optic_name))
                
                if not 'FLIPSTAT' in hdul[0].header :
                    print ("There is no 'FLIPSTAT' in the file")
                else : 
                    if hdul[0].header['FLIPSTAT'] != '        ' :
                        hdul[0].header.append('COMMENT', 
                                           'modified FLIPSTAT from {0}'.format(hdul[0].header['FLIPSTAT']), 
                                           'modified FLIPSTAT from {0}'.format(hdul[0].header['FLIPSTAT']))
                        hdul[0].header['FLIPSTAT'] = '        '
                        astro_utilities.write_log(log_file, 
                        '{1} ::: FLIPSTAT information is modified at {0}...'\
                        .format(fullname, datetime.now()))
            
                hdul.flush()  # changes are written back to original.fits
                print('#'*60)
                astro_utilities.write_log(log_file, 
                    '{1} ::: fits header is update with {0} ...'\
                    .format(fullname, datetime.now()))
    
        except Exception as err :
            print("X"*60)
            astro_utilities.write_log(err_log_file, 
                '{2} ::: \n{1} with {0} ...'\
                .format(fullname, err, datetime.now()))