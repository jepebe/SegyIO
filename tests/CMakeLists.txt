configure_file(test-data/small.sgy test-data/small.sgy COPYONLY)
configure_file(test-data/text.sgy  test-data/text.sgy COPYONLY)
configure_file(test-data/small.sgy test-data/small-traceheader.sgy COPYONLY)

add_segyio_test(utils test_utils.c)
add_segyio_test(segy test_segy.c)
add_segyio_test(segyspec test_segyspec.c)

if(BUILD_MEX)
    if(BUILD_MEX_TESTS)
        add_matlab_test(matlab.segyspec test_segyspec_mex.m test_segyspec_mex)
        add_matlab_test(matlab.segy test_segy_mex.m test_segy_mex)
    endif()
endif()


if(BUILD_PYTHON)
    add_python_test(python.segy test_segy.py)
    add_python_test(python.h.segy test_segyio_c.py)
    add_python_test(python.enum.segy test_enum.py)
    add_python_test(python.segyview test_segyview.py)
endif()
