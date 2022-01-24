"""
Motion correction script modified by TAC, original author MHT

For use with single-channel volumetric timeseries (i.e GCaMP only)
"""
import os
import sys
import time
import nibabel as nib
import numpy as np
from visanalysis.util import registration

t0 = time.time()

# first arg: path to image series base, without .suffix
#   e.g. /oak/stanford/groups/trc/data/Max/ImagingData/Bruker/20210611/TSeries-20210611-001
file_base_path = sys.argv[1]

print('Registering brain file from {}'.format(file_base_path))

# Load metadata from bruker .xml file
previous_dirs, last_dir = os.path.split(file_base_path)
if not last_dir:
    previous_dirs, last_dir = os.path.split(previous_dirs)
metadata_path = os.path.join(file_base_path, last_dir + '.xml') 
# the os.path.split returns a tuple with everything in filepath in first set and then last component in second part
metadata = registration.get_bruker_metadata(metadata_path)
print('Loaded metadata from {}'.format(metadata_path))

# Load brain images
ch1 = registration.get_ants_brain(file_base_path + 'ch1_stitched.nii', metadata, channel=0)
print('Loaded {}, shape={}'.format(file_base_path + 'ch1_stitched.nii', ch1.shape))
ch2 = registration.get_ants_brain(file_base_path + 'ch2_stitched.nii', metadata, channel=0)
print('Loaded {}, shape={}'.format(file_base_path + 'ch2_stitched.nii', ch2.shape))

# Register both channels to channel 1
merged = registration.register_two_channels_to_red(ch1, ch2, spatial_dims=len(ch1.shape) - 1)

# Register channel 1 to reference image drawn from first x frames
#merged = registration.registerOneChannelToSelf(ch1, spatial_dims=len(ch1.shape) - 1, reference_frames=20)
# # register two channels to red --this may be wrong
# merged = registration.register_two_channels_to_red(ch1, spatial_dims=len(ch1.shape) - 1, reference_frames=20)

# Save registered, merged .nii
nifti1_limit = (2**16 / 2)
if np.any(np.array(merged.shape) >= nifti1_limit): # Need to save as nifti2
    nib.save(nib.Nifti2Image(merged, np.eye(4)), file_base_path + '_reg.nii')
else: # Nifti1 is OK
    nib.save(nib.Nifti1Image(merged, np.eye(4)), file_base_path + '_reg.nii')
print('Saved registered brain to {}. Total time = {:.1f}'.format(file_base_path + '_reg.nii', time.time()-t0))
