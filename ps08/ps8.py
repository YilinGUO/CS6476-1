"""Problem Set 8: Motion History Images."""

import numpy as np
import cv2

# I/O directories
input_dir = "input"
output_dir = "output"


class MotionHistoryBuilder(object):
    """A motion history image (MHI) builder from sequential video frames."""

    def __init__(self, frame, **kwargs):
        """Initializes motion history builder object.

        Args:
            frame (numpy.array): color BGR uint8 image of initial video frame, values in [0, 255]
            kwargs: additional keyword arguments needed by builder, including:
                    - theta (float): threshold used to compute B_t. Values in [0, 255]
                    - tau (float): value to generate the MHI (M_tau). Default value set to 0.
        """

        self.mhi = np.zeros(frame.shape[:2], dtype=np.float_)  # e.g. motion history image (M_tau)
        self.theta = kwargs.get('theta', 0.)
        self.tau = kwargs.get('tau', 0.)

        # If you want to add more parameters, make sure you set a default value so that
        # your test doesn't fail the autograder because of an unknown or None value.
        #
        # The way to do it is:
        # self.some_parameter_name = kwargs.get('parameter_name', default_value)
        self.gaussian_kernel = kwargs.get('gaussian_kernel', (15, 15))
        self.gaussian_sigma_x = kwargs.get('gaussian_sigma_x', 11)
        self.prev_frame = None

    def get_b_t(self, frame, prev_frame):
        """Calculates the binary image B_t.

        In this method you will implement the equation shown in part 1 of the problem set instructions. You will use
        the class variable self.theta as the threshold value.

        Use numpy operations to speed up this process. You can implement this method without the use of loops.

        Do not perform any morphological operations here, just the equation for B_t(x, y, t).

        Args:
            frame (numpy.array): current frame defined as I_t. Can be int, or float.
            prev_frame (numpy.array): frame from last iteration defined as I_{t-1}. Can be int, or float.

        Returns:
            numpy.array: binary image containing 0s or 1s.

        """
        frame_diff = np.abs(frame.astype(np.float) - prev_frame.astype(np.float))
        # B_t(x, y) = 1 if frame - prev_frame >= theta, 0 otherwise
        # since we want to threshold greater or equal (>=), we subtract theta with 1e-5
        _, motion_image = cv2.threshold(frame_diff.astype(np.float32), self.theta - 1e-5, 1., cv2.THRESH_BINARY)
        # without using grayscale, we need to average the motion to convert from 3d to 2d
        # _, motion_image = cv2.threshold(np.mean(motion_image, axis=2).astype(np.float32), 0, 1., cv2.THRESH_BINARY)
        return motion_image

    def process(self, frame):
        """Processes a frame of video returning a binary image indicating motion areas.

        This method takes care of computing the B_t(x, y, t) and M_tau(x, y, t) as shown in the problem set
        instructions.

        B_t(x, y, t) notes:
        - Use the function get_b_t to obtain the base binary image.
        - Notice that we are using two frames: I_t and I_{t-1} which represent the current and previous frames
          respectively.
        - Because we don't have a I_{t-1} when working with the first frame, initialize and return the binary image
          creating an array of all zeros.
        - It is recommended to try morphological operations such as erode or dilate to filter the base binary
          image before working on self.mhi (M_tau)
        - This array must only contain 0 and 1 values, not a range between 0 and 1.

        M_tau(x, y, t) notes:
        - It is stored in self.mhi.
        - This array shows the motion progress using a range of values between 0 and tau.
        - When implementing the equation described in the problem set instructions you will notice that motion that
          happened recently shows as brighter areas.
        - Unlike B_t, this image is not a binary array.


        Args:
            frame: frame (numpy.array): color BGR uint8 image of current video frame, values in [0, 255].

        Returns:
            (numpy.array): binary image final B_t (type: bool or uint8), values: 0 (static) or 1 (moving).

        """
        # TODO: pass kernel size from kwargs
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, self.gaussian_kernel, self.gaussian_sigma_x)

        # if the first frame, return zeros motion_image
        if self.prev_frame is None:
            # update the prev_frame
            self.prev_frame = blurred_frame.copy()
            return np.zeros(frame.shape[:2], dtype=np.float)

        motion_image = self.get_b_t(blurred_frame, self.prev_frame)

        # update the prev frame
        self.prev_frame = blurred_frame.copy()

        # update the MHI
        self.mhi -= 1
        # if not moving, range between 0 and I(x,y,t) - 1
        _, self.mhi = cv2.threshold(self.mhi.astype(np.float32), 0., np.max(self.mhi), cv2.THRESH_TOZERO)
        # if moving
        self.mhi[np.where(motion_image >= 1.)[:2]] = self.tau

        return motion_image

    def get_mhi(self):
        """Returns the motion history image computed so far.

        Make sure the MHI is updated in process(), perform any final steps here (e.g. normalize to [0, 1])

        Returns:
            (numpy.array): float motion history image, values in [0.0, 1.0]

        """

        # Note: This method may not be called for every frame (typically, only once)
        return cv2.normalize(self.mhi, 0., 1., norm_type=cv2.NORM_MINMAX)


class Moments(object):
    """Spatial moments of an image - unscaled and scaled."""

    def __init__(self, image):
        """Initializes and computes the spatial moments on a given image.

        This method initializes the central and scaled moments using the equations shown in the problem set
        instructions.

        OpenCV functions are not allowed.

        Args:
            image (numpy.array): single-channel image, uint8 or float.
        """

        self.central_moments = np.zeros((1, 8))  # array: [mu20, mu11, mu02, mu30, mu21, mu12, mu03, mu22]
        self.scaled_moments = np.zeros((1, 8))  # array: [nu20, nu11, nu02, nu30, nu21, nu12, nu03, nu22]

        # Compute all desired moments here (recommended)
        # Note: Make sure computed moments are in correct order
        x, y = np.meshgrid(range(0, image.shape[1]), range(0, image.shape[0]))
        M10 = np.sum(np.power(x, 1) * np.power(y, 0) * image)
        M01 = np.sum(np.power(x, 0) * np.power(y, 1) * image)
        M00 = np.sum(np.power(x, 0) * np.power(y, 0) * image)
        x_bar = np.float(M10) / M00
        y_bar = np.float(M01) / M00
        x_minus_x_bar = x - x_bar
        y_minus_y_bar = y - y_bar

        mu00 = np.sum(np.power(x_minus_x_bar, 0) * np.power(y_minus_y_bar, 0) * image)

        pq = [(2, 0), (1, 1), (0, 2), (3, 0), (2, 1), (1, 2), (0, 3), (2, 2)]

        for i, (p, q) in enumerate(pq):
            self.central_moments[0, i] = np.sum(np.power(x_minus_x_bar, p) * np.power(y_minus_y_bar, q) * image)

        for i, (p, q) in enumerate(pq):
            self.scaled_moments[0, i] = np.float(self.central_moments[0, i]) / np.power(mu00, 1 + ((p + q) / 2.))

    def get_central_moments(self):
        """Returns the central moments as NumPy array.

        These are to be built in the __init__ function.

        Order: [mu20, mu11, mu02, mu30, mu21, mu12, mu03, mu22].

        Returns:
            (numpy.array): float array of central moments.

        """

        return self.central_moments

    def get_scaled_moments(self):
        """Returns scaled central moments as NumPy array.

        These are to be built in the __init__ function.

        Order: [nu20, nu11, nu02, nu30, nu21, nu12, nu03, nu22].

        Returns:
            (numpy.array): float array of scaled central moments.

        """

        return self.scaled_moments


def compute_feature_difference(a_features, b_features, scale=0.5):
    """Computes feature difference between two videos.

    This function is called by the method match_features located in experiment.py. The features used are the dictionary
    items.

    The feature difference can be seen as the euclidean distance between the input features. If you decide to use the
    scale parameter, this distance uses a weighted difference of the input features when calculating the L2 norm:

        scale * a - (1 - scale) * b


    Args:
        a_features: features from one video, MHI & MEI moments in a 16-element 1D array.
        b_features: like a_features, from other video.
        scale (float): scale factor for compute_feature_difference (if needed).

    Returns:
        diff (float): a single value, difference between the two feature vectors.

    """

    # Tip: Scale/weight difference values to get better results as moment magnitudes differ
    diff = np.sqrt(np.sum(np.square(a_features - b_features)))
    return diff
