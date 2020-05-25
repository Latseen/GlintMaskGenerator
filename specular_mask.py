# Created by: Taylor Denouden
# Organization: Hakai Institute
# Date: 2020-05-22
#
# Description: Generate masks for glint regions in in RGB Images.


import math
from pathlib import Path

import numpy as np
from PIL import Image
from fire import Fire
from scipy.ndimage.morphology import binary_opening

# For numerical stability in division ops
EPSILON = 1e-8


def estimate_specular_reflection_component(img, percent_diffuse):
    """ Estimate the specular reflection component of pixels in an image
    Based on method from:
        Wang, S., Yu, C., Sun, Y. et al. Specular reflection removal
        of ocean surface remote sensing images from UAVs. Multimed Tools
        Appl 77, 11363–11379 (2018). https://doi.org/10.1007/s11042-017-5551-7

    :param img: A numpy array of an RGB image with shape (h,w,c).
    :param percent_diffuse: An estimate of the % of pixels that show purely diffuse reflection.
    :return: An 1D image where values are an estimate of the component of specular reflectance.
    """
    # Calculate the pixel-wise max intensity and intensity range over RGB channels
    i_max = np.amax(img, axis=2)
    i_min = np.amin(img, axis=2)
    i_range = i_max - i_min

    # Calculate intensity ratio
    q = np.divide(i_max, np.clip(i_range, EPSILON, None))

    # Select diffuse only pixels using the PERCENTILE_THRESH
    # i.e. A percentage of PERCENTILE_THRESH pixels are supposed to have no
    #     specular reflection
    num_thresh = math.ceil(percent_diffuse * q.size)

    # Get indices of the percentage of pixels with lowest intensity ratio
    q_x_hat = np.partition(q.flatten(), num_thresh - 1)[num_thresh - 1]

    # Estimate the spectral component of each pixel
    spec_ref_est = np.clip(i_max - (q_x_hat * i_range), 0, None)

    # Scale value
    spec_ref_scaled = (spec_ref_est - spec_ref_est.min()) / (spec_ref_est.max() - spec_ref_est.min())

    return spec_ref_scaled


def make_mask(img_path, mask_out_path, percent_diffuse=0.2, mask_thresh=0.5, opening_iterations=2):
    """
    Create and return a glint mask for RGB imagery.

    :param img_path: The path to a named input image or directory containing images.
        Supported formats for single image processing are here:
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html.
        If img_path is a directory, all jpg, jpeg, and png images in that directory will be processed.
    :param mask_out_path: The path to send your out image including the file name and type. e.g. "/path/to/mask.png".
        mask_out_path must be a directory if img_path is specified as a directory.
    :param percent_diffuse: An estimate of the percentage of pixels in an image that show pure diffuse reflectance, and
        thus no specular reflectance (glint). Defaults to 0.5. Try playing with values, low ones typically work well.
    :param mask_thresh: The threshold on the specular reflectance estimate image to convert into a mask.
        Default is 0.5.
    :param opening_iterations: The number of morphological opening iterations on the produced mask.
        Useful for closing small holes in the mask. Set to 0 to shut off.
    :return: Numpy array of mask for results on single files, None for directory processing.
        Side effects are that the mask is saved to the specified mask_out_path location.
    """
    if Path(img_path).is_dir():
        if not Path(mask_out_path).is_dir():
            raise ValueError(
                "img_path and mask_out_path must both be a path to a directory, or both be a path to a named file.")

        # Get all images in the specified directory
        for ext in ("png", "jpg", "jpeg"):
            for path in Path(img_path).glob(f"*.{ext}"):
                out_path = Path(mask_out_path).joinpath(f"{path.stem}_mask{path.suffix}")
                _ = make_mask(str(path), str(out_path),
                              percent_diffuse=percent_diffuse, mask_thresh=mask_thresh,
                              opening_iterations=opening_iterations)

    else:
        # Open the image
        img = Image.open(img_path)

        spec_ref = estimate_specular_reflection_component(img, percent_diffuse)

        # Generate the mask
        mask = (spec_ref <= mask_thresh).astype(np.uint8)

        # Fill in small holes in the mask
        mask_closed = binary_opening(mask, iterations=opening_iterations).astype(np.uint8)

        # Save the mask
        mask_closed *= 255
        Image.fromarray(mask_closed).save(mask_out_path)

        return mask_closed


if __name__ == '__main__':
    Fire(make_mask)