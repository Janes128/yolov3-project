from voc_eval import voc_eval
import _pickle as cPickle
import numpy as np

ap = []

for i in range(1, 5):
	r,p,a = voc_eval('/home/ipvr/darknet/darknet/results/{}.txt', '/home/ipvr/darknet/darknet/trainAdd/dataset_hi/out/Images_label/{}.xml', '/home/ipvr/darknet/darknet/trainAdd/dataset_hi/data/files.txt', str(i), '.')
	print("\n--------------For the Class: " + str(i) + "--------------")
	print('Recall: ',r)
	print('Precision: ',p)
	print('Ap: ',a)
	ap += [a]

print("--------result--------")
print('Mean AP = {:.4f}'.format(np.mean(ap)))