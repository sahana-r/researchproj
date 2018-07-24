"""
Utility functions we use for our object detection system
"""

import collections
import functools
import numpy as np
import tensorflow as tf


"""
errors to catch:
directory input in arg must exist
correct version of tf
"""

# dict_for_db = {}

def populate_dict_for_db(dict_for_db, image, boxes, classes, scores, category_index, image_id=None, min_score_thresh=.5, max_boxes=20):
  """
  Inputs: 
    dict--the dict to populate
    image--numpy array representation of the image
    boxes--numpy array representing N bounding boxes; each element is made up of (ymin, xmin, ymax, xmax)
    scores--numpy array of scores for each box
    category_index--dictionary of categories
    image_id--optional parameter representing image's unique ID that we use to map it into the database category_index--dictionary
    min_score_thresh--we want scores to be higher than this threshold, which defaults to 0.5
    max_boxes--max number of boxes for this image
  """
  box_to_display_str_map = collections.defaultdict(list)
  for i in range(min(max_boxes, boxes.shape[0])):
    if scores is None or scores[i] > min_score_thresh:
      box = tuple(boxes[i].tolist())
      if classes[i] in category_index.keys():
        class_name = category_index[classes[i]]['name']
      else:
        class_name = 'N/A'
      display_str = str(class_name)
      this_label = display_str

      if image_id:
        box_ymin, box_xmin, box_ymax, box_xmax = box
        box_height = box_ymax - box_ymin
        box_width = box_xmax - box_xmin
        if image_id not in dict_for_db:
          dict_for_db[image_id] = [] 
        if [box_height, box_width, box_xmin, box_ymin, this_label, scores[i]] not in dict_for_db[image_id]:
          dict_for_db[image_id].append([float(box_height), float(box_width), float(box_xmin), float(box_ymin), this_label, float(scores[i])])
          dict_for_db[image_id] += [[float(box_height), float(box_width), float(box_xmin), float(box_ymin), this_label, float(scores[i])]]
  # print dict_for_db

# def get_dict_for_db():
#   return dict_for_db

#transform box mask to image size
def mask_transform(box_masks, boxes, img_height, img_width):
  #reshape box tensor
  boxes = tf.reshape(boxes, [-1, 2, 2])
  box_masks = tf.expand_dims(box_masks,3)
  num_boxes = tf.shape(box_masks)[0]
  #make unit-edge boxes for reference
  ref_boxes = tf.concat([tf.zeros([num_boxes, 2]), tf.ones([num_boxes, 2])], 1)
  bottom_left = tf.expand_dims(ref_boxes[:, 0:2], 1)
  top_right = tf.expand_dims(ref_boxes[:, 2:4], 1)
  #look at this line
  transformed_boxes = (boxes-bottom_left)/(top_right-bottom_left)
  reverse_boxes = tf.reshape(transformed_boxes, [-1,4])
  img_masks = tf.image.crop_and_resize(box_masks,reverse_boxes,tf.range(num_boxes), [img_height, img_width])
  return tf.squeeze(img_masks,3)





