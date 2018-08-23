import xml.etree.ElementTree as ET
import pickle
import os, glob
from os import listdir, getcwd
from os.path import join

# sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["metal_top", "metal_side", "metal_back", "metal_bottom"]

pic_dir = '/home/ipvr/darknet/darknet/trainAdd/dataset_metal/training_data_metal/images'

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('/home/ipvr/darknet/darknet/trainAdd/dataset_metal/training_data_metal/annotation/%s.xml'%(image_id))
    out_file = open('/home/ipvr/darknet/darknet/trainAdd/dataset_metal/labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()


if not os.path.exists('/home/ipvr/darknet/darknet/trainAdd/dataset_metal/labels/'):
    os.makedirs('/home/ipvr/darknet/darknet/trainAdd/dataset_metal/labels/')
# image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()

image_ids = []

for pathAndFilename in glob.iglob(os.path.join(pic_dir, "*.png")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename));
    image_ids.append(title)

list_file = open('list.txt', 'w')
for image_id in image_ids:
    list_file.write('/home/ipvr/darknet/darknet/trainAdd/dataset_metal/training_data_metal/images/%s.png'%(image_id))
    convert_annotation(image_id)
list_file.close()

