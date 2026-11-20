from collections.abc import Iterable

import numpy as np
from hdmf.utils import docval, popargs_to_dict, get_docval
from pynwb import register_class
from pynwb import TimeSeries
from pynwb.image import ImageSeries
from pynwb.core import DynamicTable, DynamicTableRegion

namespace = "ndx-facemap-motionsvd"


@register_class("MotionSVDSeries", namespace)
class MotionSVDSeries(TimeSeries):
    """
    An extension of TimeSeries to include the motion SVD components.
    """

    __nwbfields__ = ({"name": "motion_masks", "child": True},)

    @docval(
        *get_docval(TimeSeries.__init__, "name"),
        {
            "name": "data",
            "type": ("array_data", "data", TimeSeries),
            "doc": "The data values of the motion SVD temporal components."
            "Must be 2D, where the first dimension must be time,"
            "the second dimension must be the number of components.",
            "shape": (None, None),
        },
        *get_docval(TimeSeries.__init__, "description"),
        {
            "name": "motion_masks",
            "type": DynamicTableRegion,
            "doc": "References row(s) of MotionSVDMasks.",
        },
        *get_docval(
            TimeSeries.__init__,
            "resolution",
            "conversion",
            "timestamps",
            "starting_time",
            "rate",
            "comments",
            "control",
            "control_description",
            "offset",
            "unit",
        ),
    )
    def __init__(self, **kwargs):
        keys_to_set = ("motion_masks",)
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("MotionSVDMasks", namespace)
class MotionSVDMasks(DynamicTable):
    """
    An extension of DynamicTable to include the motion SVD masks.
    """

    __fields__ = (
        "downsampling_factor",
        "mask_coordinates",
        "processed_frame_dimension",
        "average_motion",
        "source_video",
    )
    __columns__ = (
        {
            "name": "image_mask",
            "description": "Mask of each component over the box given by mask_coordinates, as (height, width).",
            "index": True,
        },
        {
            "name": "singular_value",
            "description": (
                "Singular value of each component, the square root of the motion variance the component explains."
            ),
            "required": False,
        },
    )

    @docval(
        {
            "name": "name",
            "type": str,
            "doc": "Name of this MotionSVDMasks",
            "default": "MotionSVDMasks",
        },
        *get_docval(DynamicTable.__init__, "id", "columns", "colnames"),
        {
            "name": "description",
            "type": str,
            "doc": "Description of what is in this MotionSVDMasks",
            "default": "Spatial masks of the motion SVD components, one row per component.",
        },
        {
            "name": "downsampling_factor",
            "doc": "Factor by which the video was spatially downsampled in each axis before the decomposition.",
            "type": float,
        },
        {
            "name": "mask_coordinates",
            "doc": (
                "Box the masks cover in the downsampled frame, as [row_start, column_start, row_end, column_end]: "
                "0-based pixel indices, start included and end excluded."
            ),
            "type": (list, tuple, Iterable),
            "shape": (4,),
        },
        {
            "name": "processed_frame_dimension",
            "doc": "Size of the downsampled frame, as [height, width] in pixels.",
            "type": (list, tuple, Iterable),
            "shape": (2,),
        },
        {
            "name": "average_motion",
            "doc": "Mean motion of each pixel, subtracted before the decomposition, as (height, width).",
            "type": "array_data",
            "shape": (None, None),
            "default": None,
        },
        {
            "name": "source_video",
            "doc": "The behavioral video the motion SVD was computed from.",
            "type": ImageSeries,
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = (
            "downsampling_factor",
            "mask_coordinates",
            "processed_frame_dimension",
            "average_motion",
            "source_video",
        )
        args_to_set = popargs_to_dict(keys_to_set, kwargs)

        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)

    def add_row(self, **kwargs):
        """Add a component, checking its mask against mask_coordinates and processed_frame_dimension."""
        row_start, column_start, row_end, column_end = (int(value) for value in self.mask_coordinates)
        frame_height, frame_width = (int(value) for value in self.processed_frame_dimension)
        if not (0 <= row_start < row_end <= frame_height and 0 <= column_start < column_end <= frame_width):
            raise ValueError(
                f"mask_coordinates {list(self.mask_coordinates)} ([row_start, column_start, row_end, column_end]) "
                f"do not fit in a frame of [height, width] {list(self.processed_frame_dimension)}."
            )
        expected_shape = (row_end - row_start, column_end - column_start)
        mask_shape = np.shape(kwargs["image_mask"])
        if mask_shape != expected_shape:
            raise ValueError(
                f"image_mask has shape {mask_shape}, but mask_coordinates {list(self.mask_coordinates)} describe a "
                f"box of (height, width) {expected_shape}."
            )
        super().add_row(**kwargs)
