import cv2
from os import walk
from os import replace 
user_path = './zap_users'
customer_path = './customer'
for (dirpath, dirnames, filenames) in walk(customer_path):
    if len(filenames) == 0:
        print('No customer founded')
        exit()
    customer_image = cv2.imread(customer_path+'/'+filenames[0])

    for (dirp, dirn, filen) in walk(user_path):
        if len(filen) == 0:
            print('No users founded')
            exit()
        u_path = user_path+'/'+filen[0]
        user_image = cv2.imread(u_path)
        difference = cv2.subtract(customer_image, user_image)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            replace(u_path, './guilty/'+filen[0])
