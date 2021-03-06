from loader import LoaderKth
from network.topology import TopologyFolded
from network.preprocessor import Preprocessor
from network import NetworkFolded
import tensorflow as tf

# ------------------------------------------------------------------
# CONFIGURE MODEL
# ------------------------------------------------------------------

DATA_ROOT = '/workmem/'
DATA_TRAIN = DATA_ROOT + 'kth_train.hdf5'
DATA_TEST = DATA_ROOT + 'kth_test.hdf5'
SAVE_ROOT = './save/kth_frnn/'
SAVE_PATH = SAVE_ROOT + 'model/model'
TRAIN_STEPS = 500000
BATCH_SIZE = 12
DEVICE = '/gpu:0'

MODEL = NetworkFolded(topology=TopologyFolded([
    {'type': 'convolutional', 'input_shape': (64, 80, 1),    'shape': (5, 5, 1, 32),     'activation': tf.nn.tanh},
    {'type': 'convolutional', 'input_shape': (64, 80, 32),   'shape': (5, 5, 32, 64),    'activation': tf.nn.tanh},
    {'type': 'pooling',       'pool_size': (2, 2)},
    {'type': 'bconvgru',      'input_shape': (32, 40, 64),   'shape': (5, 5, 64, 128)},
    {'type': 'bconvgru',      'input_shape': (32, 40, 128),  'shape': (5, 5, 128, 128)},
    {'type': 'pooling',       'pool_size': (2, 2)},
    {'type': 'bconvgru',      'input_shape': (16, 20, 128),  'shape': (5, 5, 128, 256)},
    {'type': 'bconvgru',      'input_shape': (16, 20, 256),  'shape': (5, 5, 256, 256)},
    {'type': 'pooling',       'pool_size': (2, 2)},
    {'type': 'bconvgru',      'input_shape': (8, 10, 256),   'shape': (3, 3, 256, 512)},
    {'type': 'bconvgru',      'input_shape': (8, 10, 512),   'shape': (3, 3, 512, 512)},
    {'type': 'pooling',       'pool_size': (2, 2)},
    {'type': 'bconvgru',      'input_shape': (4, 5, 512),    'shape': (3, 3, 512, 256)},
    {'type': 'bconvgru',      'input_shape': (4, 5, 256),    'shape': (3, 3, 256, 256)},
]), scope='flownet', loss='l1')

# Prepare train data loader and preprocessor
TRAIN_PREPROCESSOR = Preprocessor([
    {'type': 'mirror', 'axes': [3]},
    {'type': 'swapaxes', 'order': [1, 0, 2, 3, 4]},
    {'type': 'rescale', 'weight': 2, 'bias': -1}
], loader=LoaderKth(DATA_TRAIN, sample_frequency=1))

# Prepare test data loader and preprocessor
TEST_PREPROCESSOR = Preprocessor([
    {'type': 'swapaxes', 'order': [1, 0, 2, 3, 4]},
    {'type': 'rescale', 'weight': 2, 'bias': -1}
], loader=LoaderKth(DATA_TEST, sample_frequency=1, shuffle_data=False))
