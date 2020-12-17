# Glint Mask Tools

![Python application](https://github.com/HakaiInstitute/glint-mask-tools/workflows/Main/badge.svg?branch=master)

## Description

GlintMaskGenerator generates image masks for regions in RGB and multispectral image files that have high levels of specular reflection.

These masks can be used in 3rd party structure-from-motion programs to replace these high glint regions with more useful data from adjacent, overlapping imagery.

## Installation

1. Go to the [releases page](https://github.com/HakaiInstitute/glint-mask-tools/releases)
2. Download the latest release file for your operating system.
3. Extract the compressed binary files from the gzipped archive.
4. This archive contains two files which provide different interfaces to the same glint mask generation program.
    4. GlintMaskGenerator-v*.\*.\*.exe provides the GUI interface
    4. glint-mask-v*.\*.\*.exe is a command line interface and has a few more advanced options available.
5. You can copy these files to any location that is convenient for you.
    5. On Linux, copying glint-mask to `user/local/bin` will allow you to call the CLI from anywhere by
       typing `glint-mask`.

### PyPi package

There also a python package version of the code available for Python 3.8 and up.

1. `pip install glint-mask-tools` to install the tools.
2. Then, `import glint_mask_tools` in your Python script.

## Usage

### GUI

In Windows, launch the GUI by double clicking the executable file. In Linux, you'll have to launch the GUI from the
terminal, e.g. `./GlintMaskGenerator`.

For now, generating masks by passing directory paths containing images is the supported workflow. Be sure to change the
image type option when processing imagery for cameras other than RGB cameras (e.g. Micasense RedEdge or DJI P4MS cameras). You will be notified of any
processing errors via a pop-up dialog.

### CLI

For information about the parameters expected by the CLI, just run `./glint-mask --help` in a bash terminal or command
line interface. All the functionality of the CLI is documented there.

#### Examples

```bash
# Get all possible camera types
glint-mask-v*.*.* --help

# Get addition parameters for, e.g., rgb_threshold method
glint-mask-v*.*.* rgb_threshold --help

# Process a directory of files
# Process rgb imagery with default parameters
glint-mask-v*.*.* rgb_threshold /path/to/dir/with/images/ /path/to/out_masks/dir/

# Process PhaseONE camera imagery with image bands split over multiple files
glint-mask-v*.*.* aco_threshold /path/to/dir/with/images/ /path/to/out_masks/dir/

# Process DJI P4MS imagery
glint-mask-v*.*.* p4ms_threshold /path/to/dir/with/images/ /path/to/out_masks/dir/

# Process Micasense RedEdge imagery 
glint-mask-v*.*.* micasense_threshold /path/to/dir/with/images/ /path/to/out_masks/dir/

# Process RGB imagery using band ratio method (see Wang, S., Yu, C., Sun, Y. et al. Specular reflection removal of ocean surface remote sensing images from UAVs. Multimedia Tools Appl 77, 11363–11379 (2018). https://doi.org/10.1007/s11042-017-5551-7)
glint-mask-v*.*.* rgb_ratio /path/to/dir/with/images/ /path/to/out_masks/dir/
```

### Python package
Installing the PyPi package allows integrating the mask generation workflow into existing python scripts with ease.

```python
from glint_mask_tools import MicasenseRedEdgeThresholdMasker
# Also available: P4MSThresholdMasker, RGBIntensityRatioMasker, RGBThresholdMasker

masker = MicasenseRedEdgeThresholdMasker(img_dir="path/to/micasense/images/", mask_dir="path/to/output/dir/",
                                         thresholds=(0.875, 1, 1, 1, 1), pixel_buffer=5)
masker.process(max_workers=5, callback=print, err_callback=print)
```

## Notes

### Directory of images processing

- All files with "jpg", "jpeg", "tif", "tiff" and "png" extensions will be processed. This can be extended as needed.
  File extension matching is case insensitive.
- Output mask files with be in the specified directory, and have the same name as the input file with "_mask" appended
  to the end of the file name stem. The file type will match the input type.

### Multi-band image processing
- For imagery types where each band is spread over multiple files, a mask will be generated for all the sibling band images.
    - For example, if a mask is generated using a threshold on the blue band image, identical masks are saved for sibling red, green, blue, nir, and red_edge bands as well.
    - If thresholds are passed for multiple bands, these mask outputs combined with a union operator before being saved for all the sibling bands associated with that capture event.

## History

TODO: Reference Kate and Toms work and give a brief history of the tool and it's development

## Bugs

This software is under active development. Bugs and feature requests can be filed on the [GitHub repository issues page](https://github.com/HakaiInstitute/glint-mask-tools/issues).

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for development and software maintenance instructions.

## Citation

Research using these tools or code should cite the following resources

TODO: bibtex citation for Kate's paper

```bibtext
@misc{Denouden2020,
  author = {Denouden, T.},
  title = {Glint Mask Generator},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/HakaiInstitute/GlintMaskGenerator}},
  commit = {8cb19e55f128da86bf0dbd312bc360ac89fe71c3}
}
```

## License
GlintMaskGenerator is released under a MIT license, as found in the [LICENSE](LICENSE) file.

---
*Created by Taylor Denouden @ Hakai Institute 2020*