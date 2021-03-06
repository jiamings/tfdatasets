import tensorflow as tf
import time
from tqdm import tqdm


def read_and_decode_single_example(filenames):
    filename_queue = tf.train.string_input_producer(filenames,
                                                    num_epochs=None)
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        features={
            'label': tf.FixedLenFeature([], tf.int64),
            'image': tf.FixedLenFeature([784], tf.float32)
        })
    label = features['label']
    image = features['image']
    return image, label


def read_and_decode(path):
    filenames = ['{}_{}.tfrecords'.format(path, i) for i in range(0, 30)]
    return read_and_decode_single_example(filenames)


if __name__ == '__main__':
    image, label = read_and_decode('/ssd_data/mnist_tfrecords/mnist')
    image_batch = tf.train.shuffle_batch([image], batch_size=100, capacity=300, min_after_dequeue=100, num_threads=4)
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        start = time.time()

        for i in tqdm(range(0, 1000)):
            img = sess.run(image_batch)

        end = time.time()
        print(end-start)
        coord.request_stop()
        coord.join(threads)