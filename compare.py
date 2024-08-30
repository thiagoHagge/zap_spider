import cv2
import os
import numpy as np

user_path = './zap_users'
customer_path = './customer'
guilty_path = './guilty'

# Ensure guilty directory exists
os.makedirs(guilty_path, exist_ok=True)

# Walk through customer directory
for (dirpath, dirnames, filenames) in os.walk(customer_path):
    if len(filenames) == 0:
        print('No customer images found.')
        break

    # Process each customer image
    for customer_file in filenames:
        customer_image_path = os.path.join(customer_path, customer_file)
        customer_image = cv2.resize(cv2.imread(customer_image_path), (224, 224)).astype(np.float32)

        # Walk through user directory
        for (dirp, dirn, filen) in os.walk(user_path):
            if len(filen) == 0:
                print('No user images found.')
                break

            # Process each user image
            for user_file in filen:
                user_image_path = os.path.join(user_path, user_file)
                user_image = cv2.resize(cv2.imread(user_image_path), (224, 224)).astype(np.float32)

                # Compare images
                difference = cv2.subtract(customer_image, user_image)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    # Move the matching image to guilty directory
                    os.replace(user_image_path, os.path.join(guilty_path, user_file))
                    print(f'Matching image found and moved: {user_file}')
                else:
                    print(f'Images are different: {user_file}')
