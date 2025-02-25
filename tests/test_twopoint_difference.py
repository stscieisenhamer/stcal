import pytest
import numpy as np

from stcal.jump.twopoint_difference import find_crs, calc_med_first_diffs


DQFLAGS = {'JUMP_DET': 4, 'SATURATED': 2, 'DO_NOT_USE': 1}


@pytest.fixture(scope='function')
def setup_cube():

    def _cube(ngroups, readnoise=10):
        nints = 1
        nrows = 204
        ncols = 204
        rej_threshold = 3
        nframes = 1
        data = np.zeros(shape=(nints, ngroups, nrows, ncols), dtype=np.float32)
        read_noise = np.full((nrows, ncols), readnoise, dtype=np.float32)
        gdq = np.zeros(shape=(nints, ngroups, nrows, ncols), dtype=np.uint32)

        return data, gdq, nframes, read_noise, rej_threshold

    return _cube


def test_nocrs_noflux(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)

    assert(0 == np.max(out_gdq))  # no CR found


def test_5grps_cr3_noflux(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)

    data[0, 0:2, 100, 100] = 10.0
    data[0, 2:5, 100, 100] = 1000
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(2 == np.argmax(out_gdq[0, :, 100, 100]))  # find the CR in the expected group


def test_5grps_cr2_noflux(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)

    data[0, 0, 100, 100] = 10.0
    data[0, 1:6, 100, 100] = 1000
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(1 == np.argmax(out_gdq[0, :, 100, 100]))  # find the CR in the expected group


def test_6grps_negative_differences_zeromedian(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)

    data[0, 0, 100, 100] = 100
    data[0, 1, 100, 100] = 90
    data[0, 2, 100, 100] = 95
    data[0, 3, 100, 100] = 105
    data[0, 4, 100, 100] = 100
    data[0, 5, 100, 100] = 100
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(0 == np.max(out_gdq))  # no CR was found


def test_5grps_cr2_negjumpflux(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)

    data[0, 0, 100, 100] = 1000.0
    data[0, 1:6, 100, 100] = 10
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(1 == np.argmax(out_gdq[0, :, 100, 100]))  # find the CR in the expected group


def test_3grps_cr2_noflux(setup_cube):
    ngroups = 3
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    data[0, 0, 100, 100] = 10.0
    data[0, 1:4, 100, 100] = 1000
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    #    assert(1,np.argmax(out_gdq[0, :, 100, 100]))  # find the CR in the expected group
    assert(np.array_equal([0, 4, 0], out_gdq[0, :, 100, 100]))


def test_4grps_cr2_noflux(setup_cube):
    ngroups = 4
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    data[0, 0, 100, 100] = 10.0
    data[0, 1:4, 100, 100] = 1000
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(1 == np.argmax(out_gdq[0, :, 100, 100]))  # find the CR in the expected group


def test_5grps_cr2_nframe2(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 2
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 500
    data[0, 2, 100, 100] = 1002
    data[0, 3, 100, 100] = 1001
    data[0, 4, 100, 100] = 1005
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 4, 0, 0], out_gdq[0, :, 100, 100]))


@pytest.mark.xfail
def test_4grps_twocrs_2nd_4th(setup_cube):
    ngroups = 4
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(np.max(out_gdq) == 4)  # a CR was found


def test_5grps_twocrs_2nd_5th(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 4], out_gdq[0, :, 100, 100]))


def test_5grps_twocrs_2nd_5thbig(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 2115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 4], out_gdq[0, :, 100, 100]))


def test_10grps_twocrs_2nd_8th_big(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 60
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 60
    data[0, 7, 100, 100] = 2115
    data[0, 8, 100, 100] = 2115
    data[0, 9, 100, 100] = 2115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 0, 0, 0, 4, 0, 0], out_gdq[0, :, 100, 100]))


def test_10grps_twocrs_10percenthit(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 2
    data[0:200, 0, 100, 100] = 10.0
    data[0:200, 1, 100, 100] = 60
    data[0:200, 2, 100, 100] = 60
    data[0:200, 3, 100, 100] = 60
    data[0:200, 4, 100, 100] = 60
    data[0:200, 5, 100, 100] = 60
    data[0:200, 6, 100, 100] = 60
    data[0:200, 7, 100, 100] = 2115
    data[0:200, 8, 100, 100] = 2115
    data[0:200, 9, 100, 100] = 2115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 0, 0, 0, 4, 0, 0], out_gdq[0, :, 100, 100]))


def test_5grps_twocrs_2nd_5thbig_nframes2(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 2115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 4], out_gdq[0, :, 100, 100]))


def test_6grps_twocrs_2nd_5th(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 115
    data[0, 5, 100, 100] = 115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert np.array_equal([0, 4, 0, 0, 4, 0], out_gdq[0, :, 100, 100])


def test_6grps_twocrs_2nd_5th_nframes2(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 115
    data[0, 5, 100, 100] = 115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 4, 0], out_gdq[0, :, 100, 100]))


def test_6grps_twocrs_twopixels_nframes2(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 100] = 10.0
    data[0, 1, 100, 100] = 60
    data[0, 2, 100, 100] = 60
    data[0, 3, 100, 100] = 60
    data[0, 4, 100, 100] = 115
    data[0, 5, 100, 100] = 115
    data[0, 0, 200, 100] = 10.0
    data[0, 1, 200, 100] = 10.0
    data[0, 2, 200, 100] = 60
    data[0, 3, 200, 100] = 60
    data[0, 4, 200, 100] = 115
    data[0, 5, 200, 100] = 115
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 4, 0], out_gdq[0, :, 100, 100]))
    assert(np.array_equal([0, 0, 4, 0, 4, 0], out_gdq[0, :, 200, 100]))


def test_5grps_cr2_negslope(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups)
    nframes = 1
    data[0, 0, 100, 100] = 100.0
    data[0, 1, 100, 100] = 0
    data[0, 2, 100, 100] = -200
    data[0, 3, 100, 100] = -260
    data[0, 4, 100, 100] = -360
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 0, 4, 0, 0], out_gdq[0, :, 100, 100]))


def test_6grps_1cr(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 1146
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert (4 == out_gdq[0, 5, 100, 100])


def test_7grps_1cr(setup_cube):
    ngroups = 7
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == out_gdq[0, 6, 100, 100])


def test_8grps_1cr(setup_cube):
    ngroups = 8
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == out_gdq[0, 6, 100, 100])


def test_9grps_1cr_1sat(setup_cube):
    ngroups = 9
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 6175
    gdq[0, 8, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == out_gdq[0, 6, 100, 100])


def test_10grps_1cr_2sat(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 6175
    data[0, 9, 100, 100] = 6175
    gdq[0, 8, 100, 100] = DQFLAGS['SATURATED']
    gdq[0, 9, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == out_gdq[0, 6, 100, 100])


def test_11grps_1cr_3sat(setup_cube):
    ngroups = 11
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 20
    data[0, 2, 100, 100] = 39
    data[0, 3, 100, 100] = 57
    data[0, 4, 100, 100] = 74
    data[0, 5, 100, 100] = 90
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 6175
    data[0, 9, 100, 100] = 6175
    data[0, 10, 100, 100] = 6175
    gdq[0, 8, 100, 100] = DQFLAGS['SATURATED']
    gdq[0, 9, 100, 100] = DQFLAGS['SATURATED']
    gdq[0, 10, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == out_gdq[0, 6, 100, 100])


def test_11grps_0cr_3donotuse(setup_cube):
    ngroups = 11
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 18
    data[0, 2, 100, 100] = 39
    data[0, 3, 100, 100] = 57
    data[0, 4, 100, 100] = 74
    data[0, 5, 100, 100] = 90
    data[0, 6, 100, 100] = 115
    data[0, 7, 100, 100] = 131
    data[0, 8, 100, 100] = 150
    data[0, 9, 100, 100] = 6175
    data[0, 10, 100, 100] = 6175
    gdq[0, 0, 100, 100] = DQFLAGS['DO_NOT_USE']
    gdq[0, 9, 100, 100] = DQFLAGS['DO_NOT_USE']
    gdq[0, 10, 100, 100] = DQFLAGS['DO_NOT_USE']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert (np.array_equal([0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, 1:-2, 100, 100]))


def test_5grps_nocr(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)


def test_6grps_nocr(setup_cube):
    ngroups = 6
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)


def test_10grps_cr2_gt3sigma(setup_cube):
    ngroups = 10
    crmag = 16
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1:11, 100, 100] = crmag
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, :, 100, 100]))


def test_10grps_cr2_3sigma_nocr(setup_cube):
    ngroups = 10
    crmag = 15
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1:11, 100, 100] = crmag
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(0 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, :, 100, 100]))


def test_10grps_cr2_gt3sigma_2frames(setup_cube):
    ngroups = 10
    crmag = 16
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 100] = 0
    data[0, 1:11, 100, 100] = crmag
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, :, 100, 100]))


def test_10grps_cr2_gt3sigma_2frames_offdiag(setup_cube):
    ngroups = 10
    crmag = 16
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 110] = 0
    data[0, 1:11, 100, 110] = crmag
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(4 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 4, 0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, :, 100, 110]))


def test_10grps_cr2_3sigma_2frames_nocr(setup_cube):
    ngroups = 10
    crmag = 15
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 2
    data[0, 0, 100, 100] = 0
    data[0, 1:11, 100, 100] = crmag
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(0 == np.max(out_gdq))  # a CR was found
    assert(np.array_equal([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], out_gdq[0, :, 100, 100]))


def test_10grps_nocr_2pixels_sigma0(setup_cube):
    ngroups = 10
    crmag = 15
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = crmag
    data[0, 1:11, 100, 100] = crmag
    read_noise[50, 50] = 0.0
    read_noise[60, 60] = 0.0
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert(0 == np.max(out_gdq))  # no CR was found


def test_5grps_satat4_crat3(setup_cube):
    ngroups = 5
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 10000
    data[0, 1, 100, 100] = 30000
    data[0, 2, 100, 100] = 60000
    data[0, 3, 100, 100] = 61000
    data[0, 4, 100, 100] = 61000
    gdq[0, 3, 100, 100] = DQFLAGS['SATURATED']
    gdq[0, 4, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    # assert(4 == np.max(out_gdq))  # no CR was found
    assert np.array_equal(
        [0, 0, DQFLAGS['JUMP_DET'], DQFLAGS['SATURATED'], DQFLAGS['SATURATED']],
        out_gdq[0, :, 100, 100])


def test_6grps_satat6_crat1(setup_cube):
    ngroups = 6
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 10000
    data[0, 1, 100, 100] = 35000  # CR
    data[0, 2, 100, 100] = 40005
    data[0, 3, 100, 100] = 45029
    data[0, 4, 100, 100] = 50014
    data[0, 5, 100, 101] = 61000
    data[0, 0, 100, 101] = 10000
    data[0, 1, 100, 101] = 15001
    data[0, 2, 100, 101] = 20003
    data[0, 3, 100, 101] = 25006
    data[0, 4, 100, 101] = 30010
    data[0, 5, 100, 101] = 35015
    gdq[0, 5, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    # assert(4 == np.max(out_gdq))  # no CR was found
    assert (np.array_equal([0, DQFLAGS['JUMP_DET'], 0, 0, 0, DQFLAGS['SATURATED']], out_gdq[0, :, 100, 100]))


@pytest.mark.xfail
def test_6grps_satat6_crat1_flagadjpixels(setup_cube):
    ngroups = 6
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 10000
    data[0, 1, 100, 100] = 35000  # CR
    data[0, 2, 100, 100] = 40005
    data[0, 3, 100, 100] = 45029
    data[0, 4, 100, 100] = 50014
    data[0, 5, 100, 101] = 61000
    data[0, 0, 100, 101] = 10000
    data[0, 1, 100, 101] = 15001
    data[0, 2, 100, 101] = 20003
    data[0, 3, 100, 101] = 25006
    data[0, 4, 100, 101] = 30010
    data[0, 5, 100, 101] = 35015
    gdq[0, 5, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    # assert(4 == np.max(out_gdq))  # no CR was found
    assert (np.array_equal([0, DQFLAGS['JUMP_DET'], 0, 0, 0, DQFLAGS['SATURATED']], out_gdq[0, :, 100, 100]))
    assert (np.array_equal([0, DQFLAGS['JUMP_DET'], 0, 0, 0, DQFLAGS['SATURATED']], out_gdq[0, :, 99, 100]))


def test_10grps_satat8_crsat3and6(setup_cube):
    ngroups = 10
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 5000
    data[0, 2, 100, 100] = 15000  # CR
    data[0, 3, 100, 100] = 20000
    data[0, 4, 100, 100] = 25000
    data[0, 5, 100, 100] = 40000  # CR
    data[0, 6, 100, 100] = 45000
    data[0, 7:11, 100, 100] = 61000
    gdq[0, 7:11, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    # assert(4 == np.max(out_gdq))  # no CR was found
    assert np.array_equal(
        [0, 0, DQFLAGS['JUMP_DET'], 0, 0, DQFLAGS['JUMP_DET'], 0,
            DQFLAGS['SATURATED'], DQFLAGS['SATURATED'], DQFLAGS['SATURATED']],
        out_gdq[0, :, 100, 100])


def test_median_with_saturation(setup_cube):
    ngroups = 10
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 4500
    data[0, 2, 100, 100] = 9100
    data[0, 3, 100, 100] = 13800
    data[0, 4, 100, 100] = 18600
    data[0, 5, 100, 100] = 40000  # CR
    data[0, 6, 100, 100] = 44850
    data[0, 7, 100, 100] = 49900
    data[0, 8:10, 100, 100] = 60000
    gdq[0, 7:10, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert (np.array_equal([0, 0, 0, 0, 0, 4, 0, 2, 2, 2], out_gdq[0, :, 100, 100]))


def test_median_with_saturation_even_num_sat_frames(setup_cube):
    ngroups = 10
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 4500
    data[0, 2, 100, 100] = 9100
    data[0, 3, 100, 100] = 13800
    data[0, 4, 100, 100] = 18600
    data[0, 5, 100, 100] = 40000  # CR
    data[0, 6, 100, 100] = 44850
    data[0, 7, 100, 100] = 49900
    data[0, 8:10, 100, 100] = 60000
    gdq[0, 6:10, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert (np.array_equal([0, 0, 0, 0, 0, 4, 2, 2, 2, 2], out_gdq[0, :, 100, 100]))


def test_median_with_saturation_odd_number_final_difference(setup_cube):
    ngroups = 9
    # crmag = 1000
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=5 * np.sqrt(2))
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 4500
    data[0, 2, 100, 100] = 9100
    data[0, 3, 100, 100] = 13800
    data[0, 4, 100, 100] = 18600
    data[0, 5, 100, 100] = 40000  # CR
    data[0, 6, 100, 100] = 44850
    data[0, 7, 100, 100] = 49900
    data[0, 8:9, 100, 100] = 60000
    gdq[0, 6:9, 100, 100] = DQFLAGS['SATURATED']
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS)
    assert (np.array_equal([0, 0, 0, 0, 0, 4, 2, 2, 2], out_gdq[0, :, 100, 100]))


def test_first_last_group(setup_cube):
    ngroups = 7
    nframes = 1
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=25.0)

    #  set up the data so that if the first and last group are used in jump
    #  detection it would cause a jump to be detected between group 1-2
    #  and group 6-7. Add a jump between 3 and 4 just to make sure jump detection is working
    #  set group 1 to be 10,000
    data[0, 0, 100, 100] = 10000.0
    #  set groups 1,2 - to be around 30,000
    data[0, 1, 100, 100] = 30000.0
    data[0, 2, 100, 100] = 30020.0
    #  set up a jump to make sure it is detected
    data[0, 3, 100, 100] = 40000.0
    data[0, 4, 100, 100] = 40020.0
    data[0, 5, 100, 100] = 40040.0
    #  set group 6 to be 50,000
    data[0, 6, 100, 100] = 50000.0

    gdq[0, 0, 100, 100] = DQFLAGS['DO_NOT_USE']
    gdq[0, 6, 100, 100] = DQFLAGS['DO_NOT_USE']
    outgdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                    rej_threshold, rej_threshold, nframes,
                                                    False, 200, 10, DQFLAGS)

    assert outgdq[0, 0, 100, 100] == DQFLAGS['DO_NOT_USE']
    assert outgdq[0, 6, 100, 100] == DQFLAGS['DO_NOT_USE']
    assert outgdq[0, 3, 100, 100] == DQFLAGS['JUMP_DET']


def test_2group(setup_cube):
    # test should not find a CR, can't do it with only one difference.
    ngroups = 2
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=25.0)

    data[0, 0, 0, 0] = 10000.0
    #  set groups 1,2 - to be around 30,000
    data[0, 1, 0, 0] = 30000.0

    outgdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                    rej_threshold, rej_threshold, nframes,
                                                    False, 200, 10, DQFLAGS)
    assert outgdq[0, 1, 0, 0] == 0
    assert outgdq[0, 0, 0, 0] == 0


def test_4group(setup_cube):
    ngroups = 4
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=25.0)

    data[0, 0, 0, 0] = 10000.0
    #  set groups 1,2 - to be around 30,000
    data[0, 1, 0, 0] = 30000.0
    data[0, 2, 0, 0] = 30020.0
    data[0, 3, 0, 0] = 30000.0

    outgdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                    rej_threshold, rej_threshold, nframes,
                                                    False, 200, 10, DQFLAGS)
    assert outgdq[0, 1, 0, 0] == 4


def test_first_last_4group(setup_cube):
    ngroups = 4
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=25.0)

    #  set up the data so that if the first and last group are used in jump
    #  detection it would cause a jump to be detected between group 0-1.
    data[0, 0, 0, 0] = 10000.0
    #  set groups 1,2 - to be around 30,000
    data[0, 1, 0, 0] = 30000.0
    data[0, 2, 0, 0] = 30020.0
    data[0, 3, 0, 0] = 30000.0
    # treat as MIRI data with first and last flagged
    gdq[0, 0, :, :] = DQFLAGS['DO_NOT_USE']
    gdq[0, 3, :, :] = DQFLAGS['DO_NOT_USE']
    outgdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                    rej_threshold, rej_threshold, nframes,
                                                    False, 200, 10, DQFLAGS)

    assert outgdq[0, 0, 0, 0] == DQFLAGS['DO_NOT_USE']
    assert outgdq[0, 3, 0, 0] == DQFLAGS['DO_NOT_USE']
    assert outgdq[0, 1, 0, 0] == 0


def test_first_last_3group(setup_cube):
    ngroups = 3
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=25.0)

    #  set up the data so that if the first and last group are used in jump
    #  detection it would cause a jump to be detected between group 1-2
    #  and group 6-7. Add a jump between 3 and 4 just to make sure jump detection is working
    #  set group 1 to be 10,000
    data[0, 0, 0, 0] = 10000.0
    data[0, 1, 0, 0] = 10100.0
    data[0, 2, 0, 0] = 30020.0

    gdq[0, 2, 0, 0] = DQFLAGS['DO_NOT_USE']  # only flag the last group
    outgdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                    rej_threshold, rej_threshold, nframes,
                                                    False, 200, 10, DQFLAGS)

    assert outgdq[0, 0, 0, 0] == 0
    assert outgdq[0, 2, 0, 0] == DQFLAGS['DO_NOT_USE']
    assert outgdq[0, 1, 0, 0] == 0


def test_10grps_1cr_afterjump(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 1190
    data[0, 9, 100, 100] = 1209

    after_jump_flag_e1 = np.full(data.shape[2:4], 1.0) * 0.0
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS,
                                                     after_jump_flag_e1=after_jump_flag_e1,
                                                     after_jump_flag_n1=10)
    # all groups after CR should be flagged
    for k in range(6, 10):
        assert 4 == out_gdq[0, k, 100, 100], f"after jump flagging failed in group {k}"


def test_10grps_1cr_afterjump_2group(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 1190
    data[0, 9, 100, 100] = 1209

    after_jump_flag_e1 = np.full(data.shape[2:4], 1.0) * 0.0
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS,
                                                     after_jump_flag_e1=after_jump_flag_e1,
                                                     after_jump_flag_n1=2)

    # 2 groups after CR should be flagged
    for k in range(6, 9):
        assert 4 == out_gdq[0, k, 100, 100], f"after jump flagging failed in group {k}"

    # rest not flagged
    for k in range(9, 10):
        assert 0 == out_gdq[0, k, 100, 100], f"after jump flagging incorrect in group {k}"


def test_10grps_1cr_afterjump_toosmall(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 21
    data[0, 3, 100, 100] = 33
    data[0, 4, 100, 100] = 46
    data[0, 5, 100, 100] = 60
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 1190
    data[0, 9, 100, 100] = 1209

    after_jump_flag_e1 = np.full(data.shape[2:4], 1.0) * 10000.0
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS,
                                                     after_jump_flag_e1=after_jump_flag_e1,
                                                     after_jump_flag_n1=10)
    # all groups after CR should be flagged
    for k in range(7, 10):
        assert 0 == out_gdq[0, k, 100, 100], f"after jump flagging incorrect in group {k}"


def test_10grps_1cr_afterjump_twothresholds(setup_cube):
    ngroups = 10
    data, gdq, nframes, read_noise, rej_threshold = setup_cube(ngroups, readnoise=10)
    nframes = 1
    data[0, 0, 100, 100] = 0
    data[0, 1, 100, 100] = 10
    data[0, 2, 100, 100] = 121
    data[0, 3, 100, 100] = 133
    data[0, 4, 100, 100] = 146
    data[0, 5, 100, 100] = 160
    data[0, 6, 100, 100] = 1160
    data[0, 7, 100, 100] = 1175
    data[0, 8, 100, 100] = 1190
    data[0, 9, 100, 100] = 1209

    after_jump_flag_e1 = np.full(data.shape[2:4], 1.0) * 500.
    after_jump_flag_e2 = np.full(data.shape[2:4], 1.0) * 10.
    out_gdq, row_below_gdq, row_above_gdq = find_crs(data, gdq, read_noise, rej_threshold,
                                                     rej_threshold, rej_threshold, nframes,
                                                     False, 200, 10, DQFLAGS,
                                                     after_jump_flag_e1=after_jump_flag_e1,
                                                     after_jump_flag_n1=10,
                                                     after_jump_flag_e2=after_jump_flag_e2,
                                                     after_jump_flag_n2=2)
    # 2 groups after CR should be flagged
    for k in range(2, 5):
        assert 4 == out_gdq[0, k, 100, 100], f"after jump flagging incorrect in group {k}"

    # all groups after CR should be flagged
    for k in range(6, 10):
        assert 4 == out_gdq[0, k, 100, 100], f"after jump flagging incorrect in group {k}"


def test_median_func():

    """
      Test the function `calc_med_first_diffs` that computes median of pixels.
      Ensure that the correct treatment based on number of non-nan diffs
      is being done, and that it works for individual pixels as well as
      pixels embedded in 3d arrays, and that it works for arrays with or
      without nans (which represent masked pixels)."""

    # single pix with 5 good diffs, should clip 1 pix and return median
    # 1d, no nans
    arr = np.array([1., 2., 3., 4., 5])
    assert calc_med_first_diffs(arr) == 2.5
    # 3d array, no nans
    arr = np.zeros(5 * 2 * 2).reshape(5, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3., 4., 5])
    assert calc_med_first_diffs(arr)[0, 0] == 2.5
    # 1d, with nans
    arr = np.array([1., 2., 3., np.nan, 4., 5, np.nan])
    assert calc_med_first_diffs(arr) == 2.5
    # 3d, with nans
    arr = np.zeros(7 * 2 * 2).reshape(7, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3., np.nan, 4., 5, np.nan])
    assert calc_med_first_diffs(arr)[0, 0] == 2.5

    # single pix with exactly 4 good diffs, should also clip 1 pix and return median
    # 1d, no nans
    arr = np.array([1., 2., 3., 4.])
    assert calc_med_first_diffs(arr) == 2
    # 3d array, no nans
    arr = np.zeros(4 * 2 * 2).reshape(4, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3., 4.])
    assert calc_med_first_diffs(arr)[0, 0] == 2
    # 1d, with nans
    arr = np.array([1., 2., 3., np.nan, 4., np.nan])
    assert calc_med_first_diffs(arr) == 2
    # 3d, with nans
    arr = np.zeros(6 * 2 * 2).reshape(6, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3., np.nan, 4., np.nan])
    assert calc_med_first_diffs(arr)[0, 0] == 2

    # single pix with exactly 3 good diffs, should compute median without clipping
    arr = np.array([1., 2., 3.])
    assert calc_med_first_diffs(arr) == 2
    # 3d array, no nans
    arr = np.zeros(3 * 2 * 2).reshape(3, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3.])
    assert calc_med_first_diffs(arr)[0, 0] == 2
    # 1d, with nans
    arr = np.array([1., 2., 3., np.nan, np.nan])
    assert calc_med_first_diffs(arr) == 2
    # 3d, with nans
    arr = np.zeros(5 * 2 * 2).reshape(5, 2, 2)
    arr[:, 0, 0] = np.array([1., 2., 3., np.nan, np.nan])
    assert calc_med_first_diffs(arr)[0, 0] == 2

    # # single pix with exactly 2 good diffs, should return the element with the minimum abs val
    arr = np.array([-1., -2.])
    assert calc_med_first_diffs(arr) == -1
    # 3d array, no nans
    arr = np.zeros(2 * 2 * 2).reshape(2, 2, 2)
    arr[:, 0, 0] = np.array([-1., -2.])
    assert calc_med_first_diffs(arr)[0, 0] == -1
    # 1d, with nans
    arr = np.array([-1., -2., np.nan, np.nan])
    assert calc_med_first_diffs(arr) == -1
    # 3d, with nans
    arr = np.zeros(4 * 2 * 2).reshape(4, 2, 2)
    arr[:, 0, 0] = np.array([-1., -2., np.nan, np.nan])
    assert calc_med_first_diffs(arr)[0, 0] == -1
