import time
import argparse
import numpy as np
import matplotlib.pyplot as plt

def get_args_parser():
    parser = argparse.ArgumentParser('Range compression of SHARAD raw data', add_help = False)
    # Paths
    parser.add_argument('--data_path', default = './data/range_compressed.npy')
    parser.add_argument('--output_path', default = './data/processed_data.npy')
    parser.add_argument('--image_path', default = './data/compressed.png')
    # Parameters
    parser.add_argument('--sampling_frequency', default = 80e6/3, type = float)
    parser.add_argument('--central_frequency', default = 20e6, type = float)
    parser.add_argument('--bandwidth', default = 10e6, type = float)
    parser.add_argument('--dielectric_eps', default = 3.15, type = float)
    parser.add_argument('--sc_height', default = 315e3)
    parser.add_argument('--sc_vel', default = 3.397e3)
    parser.add_argument('--prf', default = 135)
    # Additional
    parser.add_argument('--start', default = 400, type = int)
    parser.add_argument('--stop', default = 500, type = int)
    parser.add_argument('--aperture', default = 2, type = float, help='Aperture in seconds')
    return parser


def main(args):
    t0 = time.time()
    prf = args.prf
    R = np.load(args.data_path)
    
    aperture = int(args.aperture * prf) # in pixels
    focused = np.zeros_like(R)
    for i in range(args.start, args.stop):
        print('Column',i)
        window = R[:,i - aperture//2 : i + aperture//2]
        focused[:,i-aperture//2:i+aperture//2] += focus(window, args)
    
    np.save(args.output_path, focused)
    if args.image_path is not None:
        plt.figure(figsize=(20,20))
        plt.imshow(np.abs(focused[:,args.start:args.stop]), cmap = 'gray')
        plt.tight_layout()
        plt.savefig(args.image_path)
        plt.close()
    print('Time elapsed: {}s'.format(time.time()-t0))

    
def focus(R, args):
    c = 299792458
    v = args.sc_vel
    r = args.sc_height
    lb = c / args.central_frequency # central wavelength
    dx = c / (2 * args.bandwidth * np.sqrt(args.dielectric_eps))
    _, rangelines = R.shape
    T = rangelines / args.prf # Time of aperture in seconds
    t = np.linspace(-T/2,T/2,rangelines)

    # Range Cell Migration Correction
    R_fft = np.fft.fftshift(np.fft.fft(R, axis = 1), axes = 1)
    shifts = np.power(v * t, 2)/(2 * r) # m
    shifts_in_pixels = -np.round(shifts/dx).astype(int)*10
    R_fft_shifted = np.zeros_like(R_fft)
    for i in range(rangelines):
        R_fft_shifted[:,i] = np.roll(a = R_fft[:,i], shift = shifts_in_pixels[i], axis = 0)

    # Azimuth Compression
    k = -2 * v**2 / (lb * r)            # Slope of Doppler frequency
    fd = k * t                          # Doppler frequency vs time
    azref = np.exp(1j * np.pi * fd * t) # Azimuth reference function with given (Doppler) frequency
    azref_fft = np.fft.fftshift(np.fft.fft(azref))          # FFT of azimuth reference function
    R_focused_fft = R_fft_shifted * np.conj(azref_fft)      # Correlation of reference and signal in freq domain
    R_focused = np.fft.ifft(np.fft.fftshift(R_focused_fft, axes = 1))       # IFFT
    return R_focused

if __name__ == '__main__':
    args = get_args_parser()
    args = args.parse_args()
    main(args)