"""Unit and integration tests for the example MotionSVDSeries extension neurodata type.

TODO: Modify these tests to test your extension neurodata type.
"""

import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase, remove_test_file, NWBH5IOFlexMixin

from ndx_facemap_motionsvd import MotionSVDSeries, MotionSVDMasks


def set_up_nwbfile(nwbfile: NWBFile = None):
    """Create an NWBFile with a Device"""
    nwbfile = nwbfile or mock_NWBFile()
    return nwbfile


class TestMotionSVDSeriesConstructor(TestCase):
    """Simple unit test for creating a MotionSVDSeries."""

    def setUp(self):
        """Set up an NWB file."""
        self.nwbfile = set_up_nwbfile()
        self.behavior_module = self.nwbfile.create_processing_module(name="behavior", description="behavioral data")

    def test_constructor(self):
        """Test that the constructor for MotionSVDSeries sets values as expected."""
        n_components = 10

        motion_masks_table = MotionSVDMasks(name="MotionSVDMasks", description="motion masks")
        for _ in range(n_components):
            motion_masks_table.add_row(
                image_mask=np.random.rand(256, 256),
            )

        motion_masks = DynamicTableRegion(
            name="motion_masks", data=list(range(0, n_components)), description="all the mask", table=motion_masks_table
        )

        data = np.random.rand(100, n_components)
        motionsvd_series = MotionSVDSeries(
            name="MotionSVDSeries",
            description="description",
            data=data,
            rate=1000.0,
            motion_masks=motion_masks,
            unit="n.a.",
        )

        self.assertEqual(motionsvd_series.name, "MotionSVDSeries")
        self.assertEqual(motionsvd_series.description, "description")
        np.testing.assert_array_equal(motionsvd_series.data, data)
        self.assertEqual(motionsvd_series.rate, 1000.0)
        self.assertEqual(motionsvd_series.starting_time, 0)
        self.assertEqual(motionsvd_series.motion_masks, motion_masks)


class TestMotionSVDSeriesSimpleRoundtrip(TestCase):
    """Simple roundtrip test for MotionSVDSeries."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a MotionSVDSeries to an NWBFile, write it to file, read the file, and test that the MotionSVDSeries from the
        file matches the original MotionSVDSeries.
        """
        behavior_module = self.nwbfile.create_processing_module(name="behavior", description="behavioral data")

        n_components = 10

        motion_masks_table = MotionSVDMasks(name="MotionSVDMasks", description="motion masks")
        for _ in range(n_components):
            motion_masks_table.add_row(
                image_mask=np.random.rand(256, 256),
            )

        motion_masks = DynamicTableRegion(
            name="motion_masks", data=list(range(0, n_components)), description="all the mask", table=motion_masks_table
        )

        data = np.random.rand(100, n_components)
        motionsvd_series = MotionSVDSeries(
            name="MotionSVDSeries",
            description="description",
            data=data,
            rate=1000.0,
            motion_masks=motion_masks,
            unit="n.a.",
        )

        behavior_module.add(motion_masks_table)
        behavior_module.add(motionsvd_series)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(motionsvd_series, read_nwbfile.processing["behavior"]["MotionSVDSeries"])
            self.assertContainerEqual(motion_masks_table, read_nwbfile.processing["behavior"]["MotionSVDMasks"])

class TestMotionSVDSeriesExtensionRoundtripPyNWB(NWBH5IOFlexMixin, TestCase):
    """Complex, more complete roundtrip test for MotionSVDSeries using pynwb.testing infrastructure."""

    def getContainerType(self):
        return "MotionSVDSeries"

    def addContainer(self):
        set_up_nwbfile(self.nwbfile)
        behavior_module = self.nwbfile.create_processing_module(name="behavior", description="behavioral data")

        n_components = 10

        motion_masks_table = MotionSVDMasks(name="MotionSVDMasks", description="motion masks")
        for _ in range(n_components):
            motion_masks_table.add_row(
                image_mask=np.random.rand(256, 256),
            )

        motion_masks = DynamicTableRegion(
            name="motion_masks", data=list(range(0, n_components)), description="all the mask", table=motion_masks_table
        )

        data = np.random.rand(100,n_components)
        motionsvd_series = MotionSVDSeries(
            name="MotionSVDSeries",
            description="description",
            data=data,
            timestamps = np.linspace(0,100,100),
            motion_masks=motion_masks,
            unit="n.a.",
        )

        behavior_module.add(motion_masks_table)
        behavior_module.add(motionsvd_series)

    def getContainer(self, nwbfile: NWBFile):
        return nwbfile.processing["behavior"]["MotionSVDSeries"]