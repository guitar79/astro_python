# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 01:00:19 2018
@author: user

2019.09.29  modify - missing 'IMAGETYP' on APT

"""

import os
from datetime import datetime
from astropy.io import fits
import shutil 
import astro_utilities

add_log = True
if add_log == True :
    log_file = 'astro_Python.log'
    err_log_file = 'astro_Python_err.log'

master_file_dir_name = 'master_file_Python/'
processing_dir_name = 'processing_Python/'
integration_dir_name = 'integration_Python/'
alignment_dir_name = 'alignment_Python/'

destination_base_dir_name = "../CCD_obs_raw/"
base_dir = "../CCD_new_files/"
target_cuplicate_files_dir = "../CCD_duplicate_files/"


fullnames = astro_utilities.getFullnameListOfallFiles(base_dir)
print ("fullnames: {}".format(fullnames))
#fullname = fullnames[1110]
   
for fullname in fullnames[:]:
    if fullname[-4:] == ".txt" :
        os.remove("{}".format(fullname))
    elif fullname[-4:] == ".fit" and (os.path.isfile('{}'.format(fullname))):
        print ("Starting...   fullname: {}".format(fullname))
        new_filename = astro_utilities.get_new_filename(fullname)
        new_foldername = astro_utilities.get_new_foldername(new_filename)
        print ("new_filename: {}".format(new_filename))
        new_foldername = "{}{}".format(destination_base_dir_name, new_foldername)
        print ("new_foldername: {}".format(new_foldername))
        
        if not os.path.exists('{0}'.format(new_foldername)):
            os.makedirs('{0}'.format(new_foldername))
            astro_utilities.write_log(log_file, \
                 '{1} ::: {0} is created'.format(new_foldername, datetime.now()))    
        try :
            if os.path.exists('{0}{1}'.format(new_foldername, new_filename)):
                astro_utilities.write_log(log_file, 
                     '{0}{1} is already exist...'.format(new_foldername, new_filename))
                shutil.move(r"{}".format(fullname), r"{}{}".format(target_cuplicate_files_dir, new_filename))
                print ("move {}".format(fullname), "{}{}".format(target_cuplicate_files_dir, new_filename))
                    
            else : 
                os.rename(fullname, '{0}{1}'.format(new_foldername, new_filename))
                astro_utilities.write_log(log_file, \
                         '{0} is moved to {1}{2}'.format(fullname, new_foldername, new_filename))
                fits.setval('{0}{1}'.format(new_foldername, new_filename), \
                        'NOTES', value='modified by guitar79@naver.com')
                #fits.setval('{0}{1}'.format(new_foldername, new_filename), \
                #        'observer', value='Kiehyun Park')
                
                hdul = fits.open("{0}{1}".format(new_foldername, new_filename))
                
                print("hdul[0].header.tostring: {}".format(hdul[0].header.tostring))
                fits_info1 = hdul[0].header.tostring()
                fits_info = fits_info1.replace("'", "'\'")
                print("fits_info: {}".format(fits_info))
                
                '''
                #insert MariaDB
                conn = astro_utilities.connectMariaDB()
                cur = conn.cursor()
                tb_name = 'raw_file_info'
                remarks = ''
                cur.execute("INSERT INTO `{0}`\
                             (`ID`, `fullname`, `fits_info`, `REMARKs`) \
                             VALUES (NULL, '{1}{2}', '{3}', '{4}');"\
                             .format(tb_name, new_foldername, new_filename, fits_info, remarks))
                
                result = cur.fetchall()
                conn.commit()
                print("excute conn.commit()")
    
                cur.close()
                print("cur.close()")
                '''
                '''
                SELECT * FROM `raw_file_info` WHERE `fullname` LIKE 'aaa%'
                INSERT INTO `raw_file_info` (`ID`, `fullname`, `fits_info`, `REMARKs`) VALUES (NULL, 'aaa/aa.fit', 'fits...', 'fits... remarks');
                '''
                
                #fits.setval('{0}{1}{2}'.format(base_dir, new_foldername, new_filename), \
                #        'IMAGETYP', value='Light frame')
                print("*"*60)
                astro_utilities.write_log(log_file, \
                     '{3} ::: {0} is moved to {1}{2} ...'\
                         .format(fullname, new_foldername, new_filename, datetime.now()))
        
        except Exception as err :
            print("X"*60)
            astro_utilities.write_log(err_log_file, \
                     '{2} ::: {0} with move {1} '.format(err, fullname, datetime.now()))
                

#############################################################################
#############################################################################
#############################################################################
fullnames = astro_utilities.getFullnameListOfallsubDirs(base_dir)
print ("fullnames: {}".format(fullnames))

import shutil 

for fullname in fullnames[:] :
    fullname_el = fullname.split("/")
    if fullname_el[-1] == master_file_dir_name[:-1] : 
        #shutil.rmtree(r"{}".format(fullname))
        print ("rmtree {}\n".format(fullname))

    # Check is empty..
    if len(os.listdir(fullname)) == 0 :
        shutil.rmtree(r"{}".format(fullname)) # Delete..
        print ("rmtree {}\n".format(fullname))
    