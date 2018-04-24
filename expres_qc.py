'''
EXPRES Quality Control python module
Written by Ryan Petersburg (ryan.petersburg@yale.edu)
'''
import os
from astropy.io import fits

class EXPRES_QC(object):
    '''EXPRES Quality Control class

    Contains information about the FITS images in a given folder,
    generates plots using this info, and issues warnings when
    certain images are possibly junk.
    '''

    def __init__(self, date, raw_folder, fitspec_folder):
        self.data = data
        self.raw_folder = raw_folder
        self.fitspec_folder = fitspec_folder
        self.info_list = []

        self.fill_info()

    def fill_info(self):
        for file in os.listdir(self.raw_folder):
            if '.fit' not in file:
                continue

            info = {}

            with fits.getheader(self.raw_folder + file) as hdr:
                info['obs_id'] = hdr['OBS_ID']
                info['obj_ra'] = hdr['RA']
                info['obj_dec'] = hdr['DEC']
                info['obs_type'] = hdr['OBSTYPE']
                info['mode'] = hdr['PRESETMO']
                info['object'] = hdr['OBJECT']
                info['exp_time'] = hdr['AEXPTIME']
                info['exp_count'] = hdr['EXPCOUNT']
                info['obs_time'] = datetime.strptime(hdr['DATE-OBS'], '%Y-%m-%d %H:%M:%S')
                info['moon_dist'] = hdr['MOONDIST']
                info['sun_dist'] = hdr['SUNDIST']
                info['airmass'] = hdr['AIRMASS']

            info['reduced'] = False
            for fit_file in os.listdir(self.fitspec_folder):
                if file in fit_file:
                    info['reduced'] = True
                    break

            self.info_list.append(info)

    def generate_info_table(self)



