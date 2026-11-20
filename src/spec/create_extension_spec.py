# -*- coding: utf-8 -*-
from pathlib import Path

from pynwb.spec import NWBDatasetSpec, NWBGroupSpec, NWBLinkSpec, NWBNamespaceBuilder, export_spec


def main():
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-facemap-motionsvd""",
        version="""0.1.0""",
        doc="""extension to store the motion SVD output from FaceMap software""",
        author=[
            "Alessandra Trapani",
        ],
        contact=[
            "alessandra.trapani@catalystneuro.com",
        ],
    )
    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("ImageSeries", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")

    motion_svd_series = NWBGroupSpec(
        neurodata_type_def="MotionSVDSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include the motion SVD components.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                dtype="float",
                dims=["num_times", "num_components"],
                shape=[None, None],
                doc=(
                    "The data values of the motion SVD temporal components. Must be 2D, where the first dimension "
                    "must be time, the second dimension must be the number of components."
                ),
            ),
            NWBDatasetSpec(
                name="motion_masks",
                neurodata_type_inc="DynamicTableRegion",
                doc="References row(s) of MotionSVDMasks.",
            ),
        ],
    )

    motion_svd_masks = NWBGroupSpec(
        neurodata_type_def="MotionSVDMasks",
        neurodata_type_inc="DynamicTable",
        doc="An extension of DynamicTable to include the motion SVD masks.",
        datasets=[
            NWBDatasetSpec(
                name="image_mask",
                neurodata_type_inc="VectorData",
                dtype="float",
                dims=["rows", "columns"],
                shape=[None, None],
                doc=(
                    "Mask of each component over the box given by mask_coordinates, a (height, width) array whose "
                    "rows run down the downsampled frame and whose columns run across it. The masks of all "
                    "components are stacked along the rows, and image_mask_index marks where each one ends."
                ),
            ),
            NWBDatasetSpec(
                name="downsampling_factor",
                dtype="float",
                doc="Factor by which the video was spatially downsampled in each axis before the decomposition.",
            ),
            NWBDatasetSpec(
                name="mask_coordinates",
                dtype="int",
                dims=["row_start, column_start, row_end, column_end"],
                shape=[4],
                doc=(
                    "Box the masks cover in the downsampled frame, as [row_start, column_start, row_end, "
                    "column_end]: 0-based pixel indices, start included and end excluded, so row_end - row_start "
                    "is the height of each mask and column_end - column_start its width."
                ),
            ),
            NWBDatasetSpec(
                name="processed_frame_dimension",
                dtype="int",
                dims=["height, width"],
                shape=[2],
                doc="Size of the downsampled frame, as [height, width] in pixels: the number of rows, then columns.",
            ),
            NWBDatasetSpec(
                name="singular_value",
                neurodata_type_inc="VectorData",
                dtype="float",
                dims=["num_components"],
                shape=[None],
                doc=(
                    "Singular value of each component, the square root of the motion variance the component "
                    "explains."
                ),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="average_motion",
                dtype="float",
                dims=["height", "width"],
                shape=[None, None],
                doc=(
                    "Mean motion of each pixel, the image Facemap subtracts before the decomposition. Same shape as "
                    "each image_mask, so image_mask weighted by the MotionSVDSeries data plus this image "
                    "approximates the motion."
                ),
                quantity="?",
            ),
        ],
        links=[
            NWBLinkSpec(
                name="source_video",
                target_type="ImageSeries",
                doc="The behavioral video the motion SVD was computed from.",
                quantity="?",
            ),
        ],
    )

    new_data_types = [motion_svd_series, motion_svd_masks]

    # export the spec to yaml files in the spec folder
    output_dir = Path(__file__).parent.parent.parent / "spec"
    export_spec(ns_builder, new_data_types, str(output_dir))


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
