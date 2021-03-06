"""Problem Set 6: Optic Flow"""
import cv2
import os
import numpy as np

import ps6

# I/O directories
input_dir = "input"
output_dir = "output"


# Utility code
def quiver(u, v, scale, stride, color=(0, 255, 0)):

    img_out = np.zeros((v.shape[0], u.shape[1], 3), dtype=np.uint8)
    for y in xrange(0, v.shape[0], stride):
        for x in xrange(0, u.shape[1], stride):
            cv2.line(img_out, (x, y), (x + int(u[y, x] * scale), y + int(v[y, x] * scale)), color, 1)
            cv2.circle(img_out, (x + int(u[y, x] * scale), y + int(v[y, x] * scale)), 1, color, 1)
    return img_out


def jet_colormaps(u, v):

    stacked = np.concatenate((u, v), axis=1)
    return cv2.applyColorMap(ps6.normalize_and_scale(stacked).astype(np.uint8), cv2.COLORMAP_JET)


# Functions you need to complete:

def scale_u_and_v(u, v, level, pyr):
    """Scales up U and V arrays to match the image dimensions assigned to the first pyramid level: pyr[0].

    You will use this method in part 3. In this section you are asked to select a level in the gaussian pyramid which
    contains images that are smaller than the one located in pyr[0]. This function should take the U and V arrays
    computed from this lower level and expand them to match a the size of pyr[0].

    This function consists of a sequence of ps6.expand_image operations based on the pyramid level used to obtain
    both U and V. Multiply the result of expand_image by 2 to scale the vector values. After each expand_image
    operation you should adjust the resulting arrays to match the current level shape
    i.e. U.shape == pyr[current_level].shape and V.shape == pyr[current_level].shape. In case they don't, adjust
    the U and V arrays by removing the extra rows and columns.

    Hint: create a for loop from level-1 to 0 inclusive.

    Both resulting arrays' shapes should match pyr[0].shape.

    Args:
        u: U array obtained from ps6.optic_flow_lk
        v: V array obtained from ps6.optic_flow_lk
        level: level value used in the gaussian pyramid to obtain U and V (see part_3)
        pyr: gaussian pyramid used to verify the shapes of U and V at each iteration until the level 0 has been met.

    Returns:
        tuple: two-element tuple containing:
            u (numpy.array): scaled U array of shape equal to pyr[0].shape
            v (numpy.array): scaled V array of shape equal to pyr[0].shape
    """
    for lvl in xrange(level-1, -1, -1):
        u = ps6.expand_image(u) * 2
        v = ps6.expand_image(v) * 2

        h, w = pyr[lvl].shape
        u = u[:h, :w]
        v = v[:h, :w]

    return u, v


def part_1a():

    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'Shift0.png'), 0) / 255.
    shift_r2 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR2.png'), 0) / 255.
    shift_r5_u5 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR5U5.png'), 0) / 255.

    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 25  # Select a kernel size
    k_type = 'uniform'  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(shift_0, shift_r2, k_size, k_type, sigma)

    # Save U, V as side-by-side false-color image or single quiver plot (ps6-1-a-1.png):
    # Choose from the blocks below. One saves the results using the jet_colormap the other uses quiver plot.
    # In both cases, the resulting images should be in color. You can include both of them in your report.

    # Jet colormap
    u_v = jet_colormaps(u, v)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-a-1.png"), u_v)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-a-1.quiver.png"), u_v)

    # Now let's try with ShiftR5U5. You may want to try smoothing the input images first.
    shift_0_blurred = cv2.GaussianBlur(shift_0, (7, 7), 2)

    k_size = 45  # Select a kernel size
    k_type = 'uniform'  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(shift_0_blurred, shift_r5_u5, k_size, k_type, sigma)

    # Jet colormap
    u_v = jet_colormaps(u, v)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-a-2.png"), u_v)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-a-2.quiver.png"), u_v)


def part_1b():
    """Performs the same operations applied in part_1a using the images ShiftR10, ShiftR20 and ShiftR40.

    You will compare the base image Shift0.png with the remaining images located in the directory TestSeq:
    - ShiftR10.png
    - ShiftR20.png
    - ShiftR40.png

    Make sure you explore different parameters and/or pre-process the input images to improve your results.

    In this part you should save the following images:
    - ps6-1-b-1.png
    - ps6-1-b-2.png
    - ps6-1-b-3.png

    Returns:
        None
    """
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR40.png'), 0) / 255.

    shift_0_blurred = cv2.GaussianBlur(shift_0, (5, 5), 2)
    shift_r10_blurred = cv2.GaussianBlur(shift_r10, (5, 5), 2)
    shift_r20_blurred = cv2.GaussianBlur(shift_r20, (5, 5), 2)
    shift_r40_blurred = cv2.GaussianBlur(shift_r40, (5, 5), 2)

    # r10
    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 46  # Select a kernel size
    k_type = 'uniform'  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(shift_0_blurred, shift_r10_blurred, k_size, k_type, sigma)

    # Jet colormap
    u_v = jet_colormaps(u, v)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-1.png"), u_v)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-1.quiver.png"), u_v)

    # r20
    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 54  # Select a kernel size
    k_type = 'uniform'  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(shift_0_blurred, shift_r20_blurred, k_size, k_type, sigma)

    # Jet colormap
    u_v = jet_colormaps(u, v)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-2.png"), u_v)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-2.quiver.png"), u_v)

    # r40
    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 46  # Select a kernel size
    k_type = 'uniform'  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(shift_0_blurred, shift_r40_blurred, k_size, k_type, sigma)

    # Jet colormap
    u_v = jet_colormaps(u, v)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-3.png"), u_v)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps6-1-b-3.quiver.png"), u_v)



def part_2a_2b(save_imgs=True):

    yos_img_01 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_01.jpg'), 0) / 255.

    # 2a
    levels = 4
    yos_img_01_g_pyr = ps6.gaussian_pyramid(yos_img_01, levels)

    # 2b
    yos_img_01_l_pyr = ps6.laplacian_pyramid(yos_img_01_g_pyr)

    if save_imgs:
        yos_img_01_g_pyr_img = ps6.create_combined_img(yos_img_01_g_pyr)
        yos_img_01_l_pyr_img = ps6.create_combined_img(yos_img_01_l_pyr)
        cv2.imwrite(os.path.join(output_dir, "ps6-2-a-1.png"), yos_img_01_g_pyr_img)
        cv2.imwrite(os.path.join(output_dir, "ps6-2-b-1.png"), yos_img_01_l_pyr_img)

    return yos_img_01, yos_img_01_g_pyr, yos_img_01_l_pyr


def part_3a_1():
    yos_img_01, yos_img_01_g_pyr, yos_img_01_l_pyr = part_2a_2b(False)

    yos_img_02 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.

    levels = 4  # Define the number of levels to build the gaussian pyramid
    yos_img_02_g_pyr = ps6.gaussian_pyramid(yos_img_02, levels)

    level_id = 3  # Select the level number (or id) you wish to use
    k_size = 15  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(yos_img_01_g_pyr[level_id], yos_img_02_g_pyr[level_id],
                             k_size, k_type, sigma)  # You may use different k_size and k_type

    u, v = scale_u_and_v(u, v, level_id, yos_img_02_g_pyr)

    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    yos_img_02_warped = ps6.warp(yos_img_02, u, v, interpolation, border_mode)

    scale = 3  # define a scale value
    stride = 10  # define a stride value
    yos_img_01_02_flow = quiver(u, v, scale, stride)
    diff_yos_img_01_02 = yos_img_01 - yos_img_02_warped  # difference image

    # We will repeat the same process to obtain the difference image using yos_img_02 and yos_img_03
    yos_img_03 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_03.jpg'), 0) / 255.

    levels = 4  # Define the number of levels to build the gaussian pyramid
    yos_img_03_g_pyr = ps6.gaussian_pyramid(yos_img_03, levels)

    level_id = 3  # Select the level number (or id) you wish to use
    k_size = 15  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(yos_img_02_g_pyr[level_id], yos_img_03_g_pyr[level_id],
                             k_size, k_type, sigma)  # You may use different k_size and k_type

    u, v = scale_u_and_v(u, v, level_id, yos_img_03_g_pyr)

    scale = 3  # define a scale value
    stride = 10  # define a stride value
    yos_img_02_03_flow = quiver(u, v, scale, stride)

    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    yos_img_03_warped = ps6.warp(yos_img_03, u, v, interpolation, border_mode)
    diff_yos_img_02_03 = yos_img_02 - yos_img_03_warped

    cv2.imwrite(os.path.join(output_dir, "ps6-3-a-1.png"),
                np.concatenate((yos_img_01_02_flow, yos_img_02_03_flow), axis=0))
    cv2.imwrite(os.path.join(output_dir, "ps6-3-a-2.png"),
                np.concatenate((ps6.normalize_and_scale(diff_yos_img_01_02),
                                ps6.normalize_and_scale(diff_yos_img_02_03)), axis=0))


def part_3a_2():
    """Performs similar operations applied in part_3a_1 using the images DataSeq2/0, DataSeq2/1 and DataSeq2/2.

    This part implements the operations mentioned in the problem set which are similar to part_3a_1. In this case you
    will use the images stored in the DataSeq2 directory:
    - 0.png
    - 1.png
    - 2.png

    Make sure you explore different parameters and/or pre-process the input images to improve your results.

    In this part you should save the following images:
    - ps6-3-a-3.png
    - ps6-3-a-4.png

    Returns:
        None
    """

    dtsq2_01 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '0.png'), 0) / 255.
    dtsq2_02 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '1.png'), 0) / 255.
    dtsq2_03 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '2.png'), 0) / 255.

    # Todo: Your code here
    levels = 4
    dtsq2_01_g_pyr = ps6.gaussian_pyramid(dtsq2_01, levels)
    dtsq2_02_g_pyr = ps6.gaussian_pyramid(dtsq2_02, levels)
    dtsq2_03_g_pyr = ps6.gaussian_pyramid(dtsq2_03, levels)

    level_id = 3  # Select the level number (or id) you wish to use
    k_size = 15  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(dtsq2_01_g_pyr[level_id], dtsq2_02_g_pyr[level_id],
                             k_size, k_type, sigma)  # You may use different k_size and k_type

    u, v = scale_u_and_v(u, v, level_id, dtsq2_02_g_pyr)

    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    dtsq2_02_warped = ps6.warp(dtsq2_02, u, v, interpolation, border_mode)

    scale = 3  # define a scale value
    stride = 10  # define a stride value
    dtsq2_01_02_flow = quiver(u, v, scale, stride)
    diff_dtsq2_01_02 = dtsq2_01 - dtsq2_02_warped  # difference image

    # We will repeat the same process to obtain the difference image using dtsq2_02 and dtsq2_03
    levels = 4  # Define the number of levels to build the gaussian pyramid
    dtsq2_03_g_pyr = ps6.gaussian_pyramid(dtsq2_03, levels)

    level_id = 3  # Select the level number (or id) you wish to use
    k_size = 15  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    u, v = ps6.optic_flow_lk(dtsq2_02_g_pyr[level_id], dtsq2_03_g_pyr[level_id],
                             k_size, k_type, sigma)  # You may use different k_size and k_type

    u, v = scale_u_and_v(u, v, level_id, dtsq2_03_g_pyr)

    scale = 3  # define a scale value
    stride = 10  # define a stride value
    dtsq2_02_03_flow = quiver(u, v, scale, stride)

    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    dtsq2_03_warped = ps6.warp(dtsq2_03, u, v, interpolation, border_mode)
    diff_dtsq2_02_03 = dtsq2_02 - dtsq2_03_warped

    cv2.imwrite(os.path.join(output_dir, "ps6-3-a-3.png"),
                np.concatenate((dtsq2_01_02_flow, dtsq2_02_03_flow), axis=0))
    cv2.imwrite(os.path.join(output_dir, "ps6-3-a-4.png"),
                np.concatenate((ps6.normalize_and_scale(diff_dtsq2_01_02),
                                ps6.normalize_and_scale(diff_dtsq2_02_03)), axis=0))



def part_4a():
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR40.png'), 0) / 255.

    levels = 4  # Define the number of levels
    k_size = 25  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)

    u10, v10 = ps6.hierarchical_lk(shift_0, shift_r10, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u10_v10 = jet_colormaps(u10, v10)

    # You may want to try different parameters for the remaining function calls.
    u20, v20 = ps6.hierarchical_lk(shift_0, shift_r20, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u20_v20 = jet_colormaps(u20, v20)

    u40, v40 = ps6.hierarchical_lk(shift_0, shift_r40, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u40_v40 = jet_colormaps(u40, v40)

    jets_stacked = np.concatenate((jet_u10_v10, jet_u20_v20, jet_u40_v40), axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-a-1.png"), jets_stacked)

    # Save difference between each warped image and original image (Shift0), stacked
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    shift_r10_warped = ps6.warp(shift_r10, u10, v10, interpolation, border_mode)
    shift_r20_warped = ps6.warp(shift_r20, u20, v20, interpolation, border_mode)
    shift_r40_warped = ps6.warp(shift_r40, u40, v40, interpolation, border_mode)

    diff_0_10 = shift_r10_warped - shift_0
    diff_0_20 = shift_r20_warped - shift_0
    diff_0_40 = shift_r40_warped - shift_0

    diff_stacked = np.concatenate((ps6.normalize_and_scale(diff_0_10),
                                   ps6.normalize_and_scale(diff_0_20),
                                   ps6.normalize_and_scale(diff_0_40)),
                                  axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-a-2.png"), diff_stacked)


def part_4b():
    """Performs similar operations applied in part_4a using the images in DataSeq1.

    This part implements the operations mentioned in the problem set which are similar to part_4a. In this case you
    will use the images stored in the DataSeq1 directory and yos_img_01.jpg as the base image:
    - yos_img_01.jpg
    - yos_img_02.jpg
    - yos_img_03.jpg

    Make sure you explore different parameters and/or pre-process the input images to improve your results.

    In this part you should save the following images:
    - ps6-4-b-1.png
    - ps6-4-b-2.png

    Returns:
        None
    """

    yos_img_01 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_01.jpg'), 0) / 255.0
    yos_img_02 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.0
    yos_img_03 = cv2.imread(os.path.join(input_dir, 'DataSeq1', 'yos_img_03.jpg'), 0) / 255.0

    levels = 4  # Define the number of levels
    k_size = 35  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)

    u1, v1 = ps6.hierarchical_lk(yos_img_01, yos_img_02, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u1_v1 = jet_colormaps(u1, v1)

    # You may want to try different parameters for the remaining function calls.
    u2, v2 = ps6.hierarchical_lk(yos_img_01, yos_img_03, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u2_v2 = jet_colormaps(u2, v2)

    jets_stacked = np.concatenate((jet_u1_v1, jet_u2_v2), axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-b-1.png"), jets_stacked)

    # Save difference between each warped image and original image (Shift0), stacked
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    shift_r2_warped = ps6.warp(yos_img_02, u1, v1, interpolation, border_mode)
    shift_r3_warped = ps6.warp(yos_img_03, u2, v2, interpolation, border_mode)

    diff_1_2 = shift_r2_warped - yos_img_01
    diff_1_3 = shift_r3_warped - yos_img_01

    diff_stacked = np.concatenate((ps6.normalize_and_scale(diff_1_2),
                                   ps6.normalize_and_scale(diff_1_3)),
                                  axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-b-2.png"), diff_stacked)


def part_4c():
    """Performs similar operations applied in part_4a using the images in DataSeq2.

    This part implements the operations mentioned in the problem set which are similar to part_4a. In this case you
    will use the images stored in the DataSeq2 directory and 0.png as the base image:
    - 0.png
    - 1.png
    - 2.png

    Make sure you explore different parameters and/or pre-process the input images to improve your results.

    In this part you should save the following images:
    - ps6-4-c-1.png
    - ps6-4-c-2.png

    Returns:
        None
    """

    dtsq2_01 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '0.png'), 0) / 255.
    dtsq2_02 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '1.png'), 0) / 255.
    dtsq2_03 = cv2.imread(os.path.join(input_dir, 'DataSeq2', '2.png'), 0) / 255.

    levels = 5  # Define the number of levels
    k_size = 15  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)

    u1, v1 = ps6.hierarchical_lk(dtsq2_01, dtsq2_02, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u1_v1 = jet_colormaps(u1, v1)

    # You may want to try different parameters for the remaining function calls.
    u2, v2 = ps6.hierarchical_lk(dtsq2_01, dtsq2_03, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u2_v2 = jet_colormaps(u2, v2)

    jets_stacked = np.concatenate((jet_u1_v1, jet_u2_v2), axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-c-1.png"), jets_stacked)

    # Save difference between each warped image and original image (Shift0), stacked
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    shift_r2_warped = ps6.warp(dtsq2_02, u1, v1, interpolation, border_mode)
    shift_r3_warped = ps6.warp(dtsq2_03, u2, v2, interpolation, border_mode)

    diff_1_2 = shift_r2_warped - dtsq2_01
    diff_1_3 = shift_r3_warped - dtsq2_01

    diff_stacked = np.concatenate((ps6.normalize_and_scale(diff_1_2),
                                   ps6.normalize_and_scale(diff_1_3)),
                                  axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-4-d-2.png"), diff_stacked)


def part_5a():
    """Performs similar operations applied in part_4a using the images in Juggle.

    This part implements the operations mentioned in the problem set which are similar to part_4a. In this case you
    will use the images stored in the DataSeq2 directory and 0.png as the base image:
    - 0.png
    - 1.png
    - 2.png

    The sequence Juggle has a higher displacement between frames - the juggled balls move significantly. Try your
    hierarchical LK on that sequence and see if you can warp frame 2 back to frame 1. Apply other techniques to make
    your results better while using your LK methods.

    Try to be creative on how you can achieve good results using optic flow.

    In this part you should save the following images:
    - ps6-5-a-1.png
    - ps6-5-a-2.png

    Returns:
        None
    """

    juggle_01 = cv2.imread(os.path.join(input_dir, 'Juggle', '0.png'), 0) / 255.
    juggle_02 = cv2.imread(os.path.join(input_dir, 'Juggle', '1.png'), 0) / 255.
    juggle_03 = cv2.imread(os.path.join(input_dir, 'Juggle', '2.png'), 0) / 255.

    levels = 3  # Define the number of levels
    k_size = 25  # Select a kernel size
    k_type = "uniform"  # Select a kernel type
    sigma = 0  # Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)

    u1, v1 = ps6.hierarchical_lk(juggle_01, juggle_02, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u1_v1 = jet_colormaps(u1, v1)

    # You may want to try different parameters for the remaining function calls.
    u2, v2 = ps6.hierarchical_lk(juggle_01, juggle_03, levels, k_size, k_type, sigma, interpolation, border_mode)
    jet_u2_v2 = jet_colormaps(u2, v2)

    jets_stacked = np.concatenate((jet_u1_v1, jet_u2_v2), axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-5-a-1.png"), jets_stacked)

    # Save difference between each warped image and original image (Shift0), stacked
    interpolation = cv2.INTER_CUBIC  # Select an interpolation method (see cv2.remap)
    border_mode = cv2.BORDER_REFLECT101  # Select a pixel extrapolation method (see cv2.remap)
    shift_r2_warped = ps6.warp(juggle_02, u1, v1, interpolation, border_mode)
    shift_r3_warped = ps6.warp(juggle_03, u2, v2, interpolation, border_mode)

    diff_1_2 = shift_r2_warped - juggle_01
    diff_1_3 = shift_r3_warped - juggle_01

    diff_stacked = np.concatenate((ps6.normalize_and_scale(diff_1_2),
                                   ps6.normalize_and_scale(diff_1_3)),
                                  axis=0)
    cv2.imwrite(os.path.join(output_dir, "ps6-5-a-2.png"), diff_stacked)


if __name__ == "__main__":
    part_1a()
    part_1b()
    part_2a_2b()
    part_3a_1()
    part_3a_2()
    part_4a()
    part_4b()
    part_4c()
    part_5a()
