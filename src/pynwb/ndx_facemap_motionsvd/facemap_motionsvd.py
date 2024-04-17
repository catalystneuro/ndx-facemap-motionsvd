from collections.abc import Iterable
from hdmf.utils import docval, popargs_to_dict, get_docval
from pynwb import register_class
from pynwb import TimeSeries
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

    __fields__ = ("downsampling_factor", "mask_coordinates", "processed_frame_dimension")
    __columns__ = ({"name": "image_mask", "description": "Motion SVD mask.", "index": True},)

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
            "default": "stimulation parameters",
        },
        {
            "name": "downsampling_factor",
            "doc": "Downsampling factor used to process the behavioural video.",
            "type": float,
        },
        {
            "name": "mask_coordinates",
            "doc": "[x1, y1, x2, y2], Mask location in downsampled frame reference (top, right, bottom, left).",
            "type": (list, tuple, Iterable),
            "shape": (4,),
        },
        {
            "name": "processed_frame_dimension",
            "doc": "The dimension of the processed frame [width, height].",
            "type": (list, tuple, Iterable),
            "shape": (2,),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("downsampling_factor", "mask_coordinates", "processed_frame_dimension")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)

        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)
