import cv2
import os
import numpy as np
user_path = './zap_users'
customer_path = './customer'
guilty_counter = 0
for (dirpath, dirnames, filenames) in os.walk(customer_path):
    if len(filenames) == 0:
        print('No customer founded')
        exit()
    for name in filenames:
        customer_image = cv2.resize(cv2.imread(customer_path+'/'+name), (224, 224)).astype(np.float32)

        for (dirp, dirn, filen) in os.walk(user_path):
            if len(filen) == 0:
                print('No users founded')
                exit()
            for n in filen:
                u_path = user_path+'/'+n
                user_image = cv2.resize(cv2.imread(u_path), (224, 224)).astype(np.float32)
                difference = cv2.subtract(customer_image, user_image)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    path = './guilty'
                    if not os.path.exists(path):
                            os.makedirs(path)
                    os.replace(u_path, path+'/'+n)
                    guilty_counter = guilty_counter + 1
print(str(guilty_counter)+' guilty found')
