import cv2
import os
import imagehash
from PIL import Image
import time
from matplotlib import pyplot as plt
start_time = time.time()
# Read the video from specified path
cam = cv2.VideoCapture("D:\\pycharm_projects\\find_keyframes\\vid.mp4")
try:

    # creating a folder named data
    if not os.path.exists('data1'):
        os.makedirs('data1')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

try:

    # creating a folder named data
    if not os.path.exists('data_key_percep'):
        os.makedirs('data_key_percep')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
percep_subtraction = '0'
Hash_perc = []
Hash_perc.append(percep_subtraction)
counter_of_curr_frames = []
time_of_oper = 0
while (True):

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        print('#-------------------------------------#')
        name_curr = './data1/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name_curr)

        # writing the extracted images
        cv2.imwrite(name_curr, frame)
        # average hash
        # perception hash
        time3 = time.time()
        percep_Hash_curr = imagehash.phash(Image.open(name_curr))
        time4 = time.time()
        print('perception hash: ' + str(percep_Hash_curr))
        time_of_oper += (time4 - time3)
        print(" %s seconds " % time_of_oper)

        # start to put current hashes in a list
        currentframe_configs = str(percep_Hash_curr)
        print('configs for current frame' + name_curr)
        print(currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data1/frame' + str(prevframe) + '.jpg'
            percep_Hash_prev = imagehash.phash(Image.open(name_prev))
            # start to put previous hashes in a list
            print('configs for previous frame' + name_prev)
            prevframe_configs = str(percep_Hash_prev)

            print(prevframe_configs)

            # difference between current frame and previous one
            Hash_subtraction = str(percep_Hash_curr - percep_Hash_prev)
            percep_subtraction = str(percep_Hash_curr - percep_Hash_prev)
            Hash_perc.append(percep_subtraction)

            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)


            # Get keyframes in a folder
            if (percep_Hash_curr - percep_Hash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key_percep/frame' + str(currentframe) + '.jpg'
                print('Creating...' + name_key)
                # writing the extracted images
                cv2.imwrite(name_key, frame)
        counter_of_curr_frames.append(currentframe)
        currentframe += 1
        print('#-------------------------------------#')
    else:
        break


print(cam.get(cv2.CAP_PROP_FRAME_COUNT))
fps_amount = cam.get(cv2.CAP_PROP_FRAME_COUNT)
print(cam.get(cv2.CAP_PROP_FPS))
exec_time = (time.time() - start_time)
print("--- %s seconds ---" % exec_time)
average_time_per_oper = time_of_oper/fps_amount
print("---average time per operation: %s seconds ---" % average_time_per_oper)
plt.plot(counter_of_curr_frames, Hash_perc, label='perception Hash')
plt.xlabel("Frames")
plt.ylabel("Perception Hash substracted values")
plt.legend()
plt.show()
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()