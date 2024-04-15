"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow.compat.v1 as tf
import sys

sys.path.append('/Users/seifeddinebouragaa/Downloads/models-master/research')
sys.path.append('/Users/seifeddinebouragaa/Downloads/models-master/research/object_detection/utils')
from object_detection.utils import ops as utils_ops
from object_detection.utils import dataset_util

from PIL import Image
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
flags.DEFINE_string('label_map', '', 'Comma separated label map, e.g. label1:value1,label2:value2')
FLAGS = flags.FLAGS

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path, labelMap):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    #width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        width, height = row.width, row.height
        xmin = row.xmin / width
        xmax = row.xmax / width
        ymin = row.ymin / height
        ymax = row.ymax / height
        # sanity checks to make sure the annotations are correct
        if xmin < 0:
            print(f"[WARNING] Error with {filename.decode()}, xmin {xmin} < 0:" + row.xmin + "/" + width)
        if xmax > 1:
            print(f"[WARNING] Error with {filename.decode()}, xmax {xmax} > 1:" + row.xmax + "/" + width)
        if ymin < 0:
            print(f"[WARNING] Error with {filename.decode()}, ymin {ymin} < 0:" + row.ymin + "/" + height)
        if ymax > 1:
            print(f"[WARNING] Error with {filename.decode()}, ymax {ymax} > 1:" + row.ymax + "/" + height)
        xmins.append(xmin)
        xmaxs.append(xmax)
        ymins.append(ymin)
        ymaxs.append(ymax)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(labelMap[row['class']])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example
    
def getLabelMap(labelMapAsStr):
    labelMap = {}
    for labelValue in [x for x in labelMapAsStr.split(',')]:
        print(labelValue)
        labelMap[labelValue.split(':')[0]] = int(labelValue.split(':')[1])
    return labelMap


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    print(str(FLAGS.csv_input))
    label_map = getLabelMap(FLAGS.label_map)
    print(str(label_map))
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path, label_map)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
