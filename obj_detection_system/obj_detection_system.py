import numpy as np
import os
import sys
import tarfile
import tensorflow as tf
import zipfile


from collections import defaultdict
from io import StringIO
from PIL import Image
from multiprocessing import Process

import string_int_label_map_pb2
from google.protobuf import text_format
#import obj_detection_db and obj_detection_utils here
import obj_detection_db as db
import obj_detection_utils as util

arg = sys.argv[1]
img_dir_path = arg

img_arr = os.listdir(img_dir_path)

#try out different models
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


label_map = None
with tf.gfile.GFile(PATH_TO_LABELS, 'r') as fid:
    label_map_string = fid.read()
    label_map = string_int_label_map_pb2.StringIntLabelMap()
    try:
      text_format.Merge(label_map_string, label_map)
    except text_format.ParseError:
      label_map.ParseFromString(label_map_string)
for entry in label_map.item:
    if entry.id < 0:
        raise ValueError('Label ID must be non-negative')
    if entry.id == 0 and entry.name != 'background':
        raise ValueError('0 ID reserved for background')
categories = []
added = []
if not label_map:
    label_id_offset = 1
    for class_id in range(NUM_CLASSES):
        categories.append({'id': class_id + label_id_offset,'name': 'category_{}'.format(class_id + label_id_offset)})
for item in label_map.item:
    if not 0 < item.id <= NUM_CLASSES:
        logging.info('Ignore item %d since it falls outside of requested label range.', item.id)
        continue
    if item.HasField('display_name'):
        name = item.display_name
    else:
        name = item.name
    if item.id not in added:
        added.append(item.id)
        categories.append({'id': item.id, 'name': name})
category_index = {}
for cat in categories:
    category_index[cat['id']] = cat

def img_inference(graph, img):
    """
    inference for one image 
    """
    #move the next 2 lines just to the main function
    with graph.as_default():
        with tf.Session() as session:
            all_operations = tf.get_default_graph().get_operations()
            tensor_names = [output.name for operation in all_operations for output in operation.outputs]
            #mapping tensor name to tensor
            tensor_dict = {}
            op_keys = ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']
            for key in op_keys:
                tensor_name = key + ':0'
                if tensor_name in tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
            if 'detection_masks' in tensor_dict:
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                recast_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [recast_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [recast_num_detection, -1, -1])
                transformed_masks = util.mask_transform(detection_masks, detection_boxes, img.shape[0],img.shape[1])
                #preserve those greater than the 0.5 threshold
                transformed_masks = tf.cast(tf.greater(transformed_masks, 0.5), tf.uint8)
                #add back the one dimensions we stripped out earlier
                tensor_dict['detection_masks']=tf.expand_dims(transformed_masks, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            inference_dict = session.run(tensor_dict,{image_tensor:np.expand_dims(img, 0)})
            # type conversions
            inference_dict['num_detections'] = int(inference_dict['num_detections'][0])
            inference_dict['detection_classes'] = inference_dict['detection_classes'][0].astype(np.uint8)
            inference_dict['detection_boxes'] = inference_dict['detection_boxes'][0]
            inference_dict['detection_scores'] = inference_dict['detection_scores'][0]
            if 'detection_masks' in inference_dict:
                inference_dict['detection_masks'] = inference_dict['detection_masks'][0]
    return inference_dict


def dir_inference(dir_path, filename_arr):
    for filename in filename_arr:
        print filename
        img = Image.open(dir_path + '/' + filename)
        img_arr = np.array(img.getdata()).reshape((img.size[1], img.size[0], 3)).astype(np.uint8)
        inf_dict = img_inference(detection_graph,img)
        util.populate_dict_for_db(img, inf_dict['detection_boxes'], inf_dict['detection_classes'], inf_dict['detection_scores'], category_index, filename)




dir_inference(img_dir_path, img_arr)
d = util.get_dict_for_db()

tuples=[]

for img in d:
    obj_list = d[img]
    for obj in obj_list:
        tuples.append(tuple([img]+obj))

db.create_object_table_from_list(tuples)
db.create_topten_views()


"""
run dir inference with python multiprocessing on several groups of images to cover whole directory

populate_dict_for_db (in obj_detection_utils)

load dict into db

database utilities detailed in obj_detection_db
"""