import xml.etree.ElementTree as ET
from os import getcwd
import glob
import argparse

def convert_annotation(xml_path, list_file, image_format, class_list):
    in_file = open(xml_path, 'r')
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls_ = obj.find('name').text
        if cls_ not in class_list or int(difficult)==1:
            continue
        cls_id = class_list.index(cls_)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--train_dir', help="Path with train annotations")
	parser.add_argument('--test_dir', help="Path with test annotations")
	parser.add_argument('--class_path', help="Path for class txt file")
	parser.add_argument('--image_format', default='.png', help="Image file extension")
	args = parser.parse_args()

	# read class file
	with open(args.class_path, 'r') as f:
	    classes = f.read()
	classes = classes.split('\n')

	# output paths
	train_list_path = "train.txt"
	test_list_path = "test.txt"

	# read train and test paths
	all_train_paths = glob.glob(args.train_dir+'*.xml')
	all_test_paths = glob.glob(args.test_dir+'*.xml')
	all_train_paths = [i.replace('\\','/') for i in all_train_paths]
	all_test_paths = [i.replace('\\','/') for i in all_test_paths]

	# convert train files
	train_file = open(train_list_path, 'w')
	for i in all_train_paths:
	    image_path = i[:-4] + args.image_format
	    train_file.write(image_path)
	    convert_annotation(i, train_file, args.image_format, classes)
	    train_file.write('\n')
	train_file.close()

	# convert test files
	test_file = open(test_list_path, 'w')
	for i in all_test_paths:
	    image_path = i[:-4] + args.image_format
	    test_file.write(image_path)
	    convert_annotation(i, test_file, args.image_format, classes)
	    test_file.write('\n')
	test_file.close()


if __name__ == '__main__':
	main()
