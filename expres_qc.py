'''
EXPRES Quality Control python module
Written by Ryan Petersburg (ryan.petersburg@yale.edu)
'''
import os
import numpy as np
from astropy.io import fits

class Image_Info(object):
    '''EXPRES image information class

    Contains information about the raw FITS image as well as
    the related reduced/extracted data if it exists
    '''

    def __init__(self, raw_file, fitspec_folder):
        self.raw_file = raw_file
        self.fitspec_folder = fitspec_folder

        self.set_info()

    def set_info(self):

        self.header = fits.getheader(self.raw_file)

        self.obs_id = self.header['OBS_ID']
        if self.obs_id not in self.raw_file:
            raise RuntimeError('observation IDs do not match: {}, {}'.format(self.obs_id, self.raw_file))

        self.object = self.header['OBJECT']
        self.obs_time = datetime.strptime(self.header['DATE-OBS'], '%Y-%m-%d %H:%M:%S')
        self.exp_counts = self.header['EXPCOUNT']

        with fits.open(self.raw_file) as hdul:
            self.max_counts = np.max(hdul[0].data)
            self.min_counts = np.min(hdul[0].data)

        self.reduced = False
        for fit_file in os.listdir(self.fitspec_folder):
            if self.obs_id in fit_file:
                self.reduced = True
                break

class EXPRES_QC(object):
    '''EXPRES Quality Control class

    Contains information about the FITS images in a given folder,
    generates plots using this info, and issues warnings when
    certain images are possibly junk.
    '''

    def __init__(self, date, raw_folder, fitspec_folder):
        self.date = date
        self.raw_folder = raw_folder
        self.fitspec_folder = fitspec_folder
        self.info_list = []

        self.fill_info()

    def fill_info(self):
        for file in os.listdir(self.raw_folder):
            if '.fit' not in file:
                continue
            self.info_list.append(Image_Info(self.raw_folder + file,
                                             self.fitspec_folder))

    def generate_info_table(self):
        pass

    def generate_counts_plot(self, mode, ax=None):

        counts = []
        for info in self.info_list:
            if info['mode'] == mode:
                counts.append(info.exp_counts)

        if ax is None:
            plt.figure()
            plt.plot(counts)
            plt.show()
        else:
            ax.plot(counts)


