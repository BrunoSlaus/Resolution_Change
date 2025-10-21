from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, FK5
from astropy import units as u
import astropy
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import sys

import warnings
warnings.filterwarnings("ignore")

from reproject import reproject_interp

##########################################################################################################
Image_Folder       = 'Input/Galaxy_Images_VLA/'


Resolution_Rescale_Factor = 0.2
Interpolation_Order = 'bilinear'        #'bilinear', 'biquadratic', 'bicubic' or 'nearest-neighbor'
##########################################################################################################

#Removing old stuff
subprocess.call('rm -rf Output/*', shell=True)
subprocess.call('rm -f log/*', shell=True)

Galaxy_Names = [file for file in os.listdir(Image_Folder) if not file.startswith('.')]
print('\nStarting the Resolution Change of ' + str(len(Galaxy_Names)) + ' galaxies.')
print('Resolution rescaled by     : ' + str(Resolution_Rescale_Factor))
print('Interpolation Order set to : ' + Interpolation_Order + ' \n')

logfile = open('log/log.txt','a')
logfile.write('Starting the log file for the Resolution-Change code.\n')
logfile.write('Resolution changed by a factor of : ' + str(Resolution_Rescale_Factor) + '\n')
logfile.write('Interpolation Order set to        : ' + Interpolation_Order + ' \n')


galaxy_index = 0
for galaxy in Galaxy_Names:
    filename  = [file for file in os.listdir(Image_Folder + galaxy) if not file.startswith('.')]
    directory = Image_Folder + galaxy + '/' + filename[0]
    logfile.write('\n\nGALAXY: ' + galaxy)
    logfile.write('\nDirectory of the galaxy image: ' + directory)
    
    galaxy_index = galaxy_index + 1
    sys.stdout.write('\rChanging resolution for galaxy: ' + str(galaxy_index) +'/'+ str(len(Galaxy_Names)))  
    sys.stdout.flush()
            
    hdul1 = fits.open(directory)
    hdu1  = hdul1[0]
    hdr1  = hdu1.header

    hdul2 = fits.open(directory)
    hdu2  = hdul2[0]
    hdr2  = hdu2.header
    
    rescaled_hdr = hdr2
    rescaled_hdr['NAXIS1'] = int(rescaled_hdr['NAXIS1'] * Resolution_Rescale_Factor) + 1
    rescaled_hdr['CRPIX1'] = int(rescaled_hdr['CRPIX1'] * Resolution_Rescale_Factor) + 1
    rescaled_hdr['CDELT1'] = rescaled_hdr['CDELT1'] / Resolution_Rescale_Factor    
        
    rescaled_hdr['NAXIS2'] = int(rescaled_hdr['NAXIS2'] * Resolution_Rescale_Factor) + 1
    rescaled_hdr['CRPIX2'] = int(rescaled_hdr['CRPIX2'] * Resolution_Rescale_Factor) + 1
    rescaled_hdr['CDELT2'] = rescaled_hdr['CDELT2'] / Resolution_Rescale_Factor
  
  

    logfile.write('\nOld header: ' )  
    logfile.write('\nNAXIS1: ' + str(hdr1['NAXIS1']))    
    logfile.write('\nCRPIX1: ' + str(hdr1['CRPIX1']))    
    logfile.write('\nCDELT1: ' + str(hdr1['CDELT1']))        
    logfile.write('\nNAXIS2: ' + str(hdr1['NAXIS2']))    
    logfile.write('\nCRPIX2: ' + str(hdr1['CRPIX2']))    
    logfile.write('\nCDELT2: ' + str(hdr1['CDELT2']))     
    logfile.write('\nNew header: ' )  
    logfile.write('\nNAXIS1: ' + str(rescaled_hdr['NAXIS1']))    
    logfile.write('\nCRPIX1: ' + str(rescaled_hdr['CRPIX1']))    
    logfile.write('\nCDELT1: ' + str(rescaled_hdr['CDELT1']))        
    logfile.write('\nNAXIS2: ' + str(rescaled_hdr['NAXIS2']))    
    logfile.write('\nCRPIX2: ' + str(rescaled_hdr['CRPIX2']))    
    logfile.write('\nCDELT2: ' + str(rescaled_hdr['CDELT2'])) 
 
 
              
    wcs_ref = WCS(rescaled_hdr)                       
    reprojected_image, reprojected_footprint = reproject_interp(hdu1, wcs_ref, order = Interpolation_Order)
    
    subprocess.call('mkdir Output/' + galaxy, shell=True)    
    fits.writeto('Output/' + galaxy + '/' + galaxy + '.fits', reprojected_image, rescaled_hdr, overwrite=True)   


print('\n\n')


