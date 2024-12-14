import sys
import dlib
import os
import cv2
import face_alignment
from multiprocessing import Pool, Process, Queue
import time
import torch
from tqdm import tqdm


def run(files):
    #os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False, device=device)
    #print('gpu={},n_files={}'.format(gpu, len(files)))
    #print('n_files={}'.format(len(files)))
    tic = time.time()
    count = 0
    for (img_name, savename) in tqdm(files, desc="Processing files"):
        I = cv2.imread(img_name)
        points_list = fa.get_landmarks(I)
        
        with open(savename, 'w') as f:
            if(points_list is not None):
                for points in points_list:
                    for (x, y) in points:
                        f.write('({}, {})\t'.format(x, y))
                    f.write('\n')

        count += 1
        if(count % 1000 == 0):
            print('dst={},eta={}'.format(savename, (time.time()-tic)/(count) * (len(files) - count) / 3600.0))
       

if(__name__ == '__main__'):
    with open('imgs.txt', 'r') as f:
        data = [line.strip() for line in f.readlines()]
    
    data = [(name, name.replace('.jpg', '.txt')) for name in data]
    for (_, dst) in data:
        dir, _ = os.path.split(dst)
        if(not os.path.exists(dir)):
            os.makedirs(dir)

#    p = Process(target=run, args=(data,))
#    p.start()
#    p.join()
    processes = []
    n_p = 4
    #gpus = ['1', '2', '3']
    bs = len(data) // n_p
    for i in range(n_p):
        if(i == n_p - 1):
            bs = len(data)
        #p = Process(target=run, args=(gpus[i],data[:bs],))
        p = Process(target=run, args=(data[:bs],))
        data = data[bs:]
        p.start()
        processes.append(p)
    assert(len(data) == 0)
    for p in processes:
        p.join()
