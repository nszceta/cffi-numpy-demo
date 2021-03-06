import sys
import numpy
import cffi
ffi = cffi.FFI()

with open('imgsample.h') as my_header:
    ffi.cdef(my_header.read())

with open('imgsample.c') as my_source:
    if __debug__:
        print('Building the debug build...')
        ffi.set_source(
            '_imgsample',
            my_source.read(),
            extra_compile_args=['-Werror', '-pedantic', '-Wall', '-g', '-O0']
        )
    else:
        print('Building for performance without OpenMP...')
        ffi.set_source(
            '_imgsample',
            my_source.read(),
            extra_compile_args=['-Ofast']
        )

ffi.compile()  # convert and compile - mandatory!

import _imgsample

# window size 2
# 2D array

my_input = numpy.array(
    [
        [1,   2,  3,  4],
        [5,   6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=numpy.float32
)

window_size = 2
sample_count = (my_input.shape[0] - window_size + 1) * (my_input.shape[1] - window_size + 1)
print('window_size -> ' + str(window_size) + ' ... sample_count -> ' + str(sample_count))
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', my_input.ctypes.data)
_my_output = _imgsample.ffi.cast('float *', my_output.ctypes.data)

_imgsample.lib.sample2d(_x, _y, _window_size, _my_input, _my_output)
print('testing with window size -> 2')
assert numpy.array_equal(my_output[0], [[1,2],[5,6]])
assert numpy.array_equal(my_output[sample_count-1], [[11,12],[15,16]])

# window size 3
# 2D array

my_input = numpy.array(
    [
        [1,   2,  3,  4],
        [5,   6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=numpy.float32
)

window_size = 3
sample_count = (my_input.shape[0] - window_size + 1) * (my_input.shape[1] - window_size + 1)
print('window_size -> ' + str(window_size) + ' ... sample_count -> ' + str(sample_count))
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', my_input.ctypes.data)
_my_output = _imgsample.ffi.cast('float *', my_output.ctypes.data)

_imgsample.lib.sample2d(_x, _y, _window_size, _my_input, _my_output)
assert numpy.array_equal(my_output[0], [[1,2,3],[5,6,7],[9,10,11]])
assert numpy.array_equal(my_output[sample_count-1], [[6,7,8],[10,11,12],[14,15,16]])

# window size 10 
# big 2D array

my_input = numpy.random.rand(4000,4000).astype(numpy.float32)
window_size = 10

sample_count = (my_input.shape[0] - window_size + 1) * (my_input.shape[1] - window_size + 1)
print('window_size -> ' + str(window_size) + ' ... sample_count -> ' + str(sample_count))
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', my_input.ctypes.data)
_my_output = _imgsample.ffi.cast('float *', my_output.ctypes.data)

_imgsample.lib.sample2d(_x, _y, _window_size, _my_input, _my_output)

# window size 2
# RGB array (3D)

my_input = numpy.array(
    [
        [[1,2,3],[5,6,7],[4,5,6],[6,4,5]],
        [[4,6,3],[5,8,7],[6,3,6],[5,8,5]],
        [[3,7,3],[4,5,7],[5,2,5],[4,5,5]],
        [[2,8,3],[3,2,7],[1,2,6],[3,1,5]],
    ], dtype=numpy.float32
)

window_size = 2
sample_count = 3 * (my_input.shape[0] - window_size + 1) * (my_input.shape[1] - window_size + 1)
print('window_size -> ' + str(window_size) + ' ... sample_count -> ' + str(sample_count))
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', my_input.ctypes.data)
_my_output = _imgsample.ffi.cast('float *', my_output.ctypes.data)

_imgsample.lib.sample3d(_x, _y, _window_size, _my_input, _my_output)
assert numpy.array_equal(
    my_output[0],
    [
        [[1,2,3],[5,6,7]],
        [[4,6,3],[5,8,7]],
    ]
)
assert numpy.array_equal(
    my_output[sample_count-1],
    [
        [[5,2,5],[4,5,5]],
        [[1,2,6],[3,1,5]],
    ]
)

# window size 10
# big RGB array (3D)

my_input = numpy.random.rand(1000,1000,3).astype(numpy.float32)
window_size = 20

sample_count = 3 * (my_input.shape[0] - window_size + 1) * (my_input.shape[1] - window_size + 1)
print('window_size -> ' + str(window_size) + ' ... sample_count -> ' + str(sample_count))
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', my_input.ctypes.data)
_my_output = _imgsample.ffi.cast('float *', my_output.ctypes.data)

_imgsample.lib.sample3d(_x, _y, _window_size, _my_input, _my_output)

