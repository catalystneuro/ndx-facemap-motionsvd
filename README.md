# ndx-facemap-motionsvd Extension for NWB

The NWB extension for storing the motion SVD output from FaceMap software

## Installation

pip install ndx_facemap_motionsvd

## Usage

```python
from uuid import uuid4
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

from pynwb import NWBFile, NWBHDF5IO
from pynwb.core import DynamicTableRegion

from ndx_facemap_motionsvd import MotionSVDSeries, MotionSVDMasks

# Create NWBFile
nwbfile = NWBFile(
    session_description="session_description",
    identifier=str(uuid4()),
    session_start_time=datetime(1970, 1, 1, tzinfo=tzlocal()),
)

# Create behavior processing module
behavior_module = nwbfile.create_processing_module(name="behavior", description="behavioral data")

n_components = 10

# Create MotionSVDMasks
motion_masks_table = MotionSVDMasks(
    name="MotionSVDMasks",
    description="motion masks",
    downsampling_factor=4.0,
    mask_coordinates=[0, 0, 256, 256],
    processed_frame_dimension=[256, 256],
)
for _ in range(n_components):
    motion_masks_table.add_row(
        image_mask=np.random.rand(256, 256),
    )

motion_masks = DynamicTableRegion(
    name="motion_masks", data=list(range(0, n_components)), description="all the mask", table=motion_masks_table
)

# Create MotionSVDSeries
data = np.random.rand(100, n_components)
motionsvd_series = MotionSVDSeries(
    name="MotionSVDSeries",
    description="description",
    data=data,
    rate=1000.0,
    motion_masks=motion_masks,
    unit="n.a.",
)

# Add to the NWBFile
behavior_module.add(motion_masks_table)
behavior_module.add(motionsvd_series)

# Write LabMetaData to NWB file
nwbfile_path = "facemap_motionsvd.nwb"
with NWBHDF5IO(nwbfile_path, mode="w") as io:
    io.write(nwbfile)

# Check LabMetaData was added to the NWB file
with NWBHDF5IO(nwbfile_path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    read_nwbfile_motionsvd_series = read_nwbfile.processing["behavior"]["MotionSVDSeries"]
    read_nwbfile_motionsvd_masks = read_nwbfile.processing["behavior"]["MotionSVDMasks"]


```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
