import numpy as np 

left = int(np.sum(list([0,0,0,0,0,1020])))
right = int(np.sum(list([0,0,0,0,0,0])))

print ("{}|--({})--|{} ".format(left,abs(right-left),right))