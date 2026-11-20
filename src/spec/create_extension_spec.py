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
                shape=[None, None],
                doc="motion SVD mask.",
            ),
            NWBDatasetSpec(
                name="downsampling_factor",
                dtype="float",
                doc="Downsampling factor used to process the behavioural video.",
            ),
            NWBDatasetSpec(
                name="mask_coordinates",
                dtype="int",
                shape=[4],
                doc="(x1, y1, x2, y2), Mask location in downsampled frame reference (top, right, bottom, left).",
            ),
            NWBDatasetSpec(
                name="processed_frame_dimension",
                dtype="int",
                shape=[2],
                doc="The dimension of the processed frame [width, height].",
            ),
            NWBDatasetSpec(
                name="singular_value",
                neurodata_type_inc="VectorData",
                dtype="float",
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
