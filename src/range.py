import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

def get_args_parser():
    parser = argparse.ArgumentParser('Range compression of SHARAD raw data', add_help = False)
    # Paths
    parser.add_argument('--chirp_path', default = './data/reference_chirp_p00tx_p00rx.dat')
    parser.add_argument('--data_path', default = './data/raw_data.npy')
    parser.add_argument('--topo_path', default='./data/topo.npy')
    parser.add_argument('--output_path', default = './data/range_compressed.npy')
    parser.add_argument('--image_path', default = './data/compressed.png')
    # Parameters
    parser.add_argument('--presum', default = 4, type = int)
    parser.add_argument('--bits_per_sample', default = 8, type = int)
    parser.add_argument('--sampling_frequency', default = 80e6/3, type = float)
    parser.add_argument('--central_frequency', default = 20e6, type = float)
    parser.add_argument('--dielectric_eps', default = 3.15, type = float)
    return parser

def main(args):
    t0 = time.time()
    c = 299792458
    R = np.load(args.data_path)
    samples, rangelines = R.shape
    sf = args.sampling_frequency
    si = 1/sf
    cf = args.central_frequency
    
    # Decompression (for fixed scaling)
    p = args.presum
    b = args.bits_per_sample
    R = R * np.exp2(np.round(np.log2(p)) - b + 8) / p
    R = R - R.mean()

    # Topographic shift
    topo = np.load(args.topo_path) * 1000 # in meters
    topo = topo - topo.min()
    dz = c / np.sqrt(args.dielectric_eps) * si
    pixel_topo = topo/dz # Topographic shift in pixels
    for i in range(R.shape[1]):
        R[:,i] = np.roll(R[:,i], shift = -int(np.round(pixel_topo[i])))

    # Loading chirp file from SHARAD calibration folder (Mars ODE)
    chirpf = args.chirp_path
    POINTS = 2048
    C = np.zeros((2,POINTS)) # first row is real, second row is imaginary
    with open(chirpf, 'rb') as fid:
        C[0,:] = np.fromfile(fid, dtype='<f4', count=POINTS, offset= 0)
    with open(chirpf, 'rb') as fid:
        C[1,:] = np.fromfile(fid, dtype='<f4', count=POINTS, offset= POINTS*4)
    chirp = C[0,:] + 1j*C[1,:] # Spectrum of the chirp

    # Pad and time interval
    to_nearest_p2 = 2 ** int(np.ceil(np.log2(samples)))
    pad_len = (to_nearest_p2 - samples) // 2
    to_pad = np.zeros((pad_len, rangelines))
    R = np.concatenate([to_pad, R, to_pad], axis = 0)
    new_n_samples = R.shape[0]
    T = si * new_n_samples
    t_signal = np.linspace(0,T - 1/sf, new_n_samples)
    
    # Range compression
    R_complex = R * np.exp(2 * np.pi * (sf-cf)/1e6 *1j * t_signal)[:,np.newaxis]    # Complex demodulation
    signal_fft = np.fft.fft(R_complex, axis = 0)                                # Signal FFT
    signal_fft = signal_fft[1024:3072,:]                                        # Keep only signal central frequencies
    chirp_conj = np.fft.fftshift(np.conj(chirp))                                # Chirp spectrum conjugate
    RC_fft = chirp_conj[:,np.newaxis] * signal_fft                # Multiplication between Signal FFT and Chirp spectrum conjugate

    # Hann windowing
    hann_window = np.hanning(RC_fft.shape[0])[:,np.newaxis]
    RC_windowed = RC_fft * np.fft.fftshift(hann_window)
    RC = np.fft.ifft(RC_windowed, axis = 0)

    # Save
    np.save(args.output_path, RC)
    if args.image_path is not None:
        plt.figure(figsize=(20,20))
        plt.imshow(np.abs(RC), cmap = 'gray', aspect = 'auto')
        plt.tight_layout()
        plt.savefig(args.image_path)
        plt.close()
    print('Time elapsed: {}s'.format(time.time()-t0))
    
if __name__ == '__main__':
    args = get_args_parser()
    args = args.parse_args()
    main(args)