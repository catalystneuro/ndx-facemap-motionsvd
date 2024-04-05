# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
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
    ns_builder.include_namespace("core")

    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    motionsvd_series = NWBGroupSpec(
        neurodata_type_def="MotionSVDSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include the motion SVD components.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="motion SVD temporal components.",
                dtype="float",
                shape=(None, 2),
            )
        ],
    )
    motionsvd_masks = NWBGroupSpec(
        neurodata_type_def="MotionSVDMasks",
        neurodata_type_inc="DynamicTable",
        doc="An extension of DynamicTable to include the motion SVD masks.",
        datasets=[
            NWBDatasetSpec(
                name="image_mask",
                doc="motion SVD mask.",
                dtype="float",
                shape=(None, 2),
                neurodata_type_inc="VectorData",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [motionsvd_series,motionsvd_masks]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
