#coding=utf-8
import requests
import time
import json
import base64
import cv2
import os
from scipy import misc

num = 1
mtcnn_elapsed = 0
facenet_elapsed = 0
emotion_elapsed = 0
eye_elapsed = 0
angle_elapsed = 0
alltime = 0

i = 0
start = time.time()
for i in xrange(num):
    start = time.clock()
    s = requests
    
    imagepath = '/data/ligang/detectron/Detectron-master/restful/benchmark/'
    imagepath_post = '/opt/ligang/detectron/Detectron-master/restful/benchmark/'
    imagepath_out = '/data/ligang/detectron/Detectron-master/restful/out/'
    files= os.listdir(imagepath)
    for file in files:
        if file.endswith('.jpg'):
            print(file)
            image = os.path.join(imagepath_post,file)
            data={"data":image}
            my_json_data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            r = s.post('http://192.168.200.213:9527/user', headers=headers,data = my_json_data,)
            #print type(r)
            #print (r)
            #print type(r.json())
            
            
            #print (r.json())
            print (i)
            i = i+1
            #add plot
            img = cv2.imread(os.path.join(imagepath,file))
            data= {}
            data = r.json()
            datalist = []
            datalist = data['data']
            print(len(datalist))
            for j in xrange(len(datalist)):
                singledata = {}
                boxdict = {}
                singledata = datalist[j]
                boxdict = singledata['bbox']
                xmin = boxdict['xmin']
                ymin = boxdict['ymin']
                xmax = boxdict['xmax']
                ymax = boxdict['ymax']
                cv2.rectangle(img, (xmin,ymin), (xmax,ymax),(0,255,0))
                
                font= cv2.FONT_HERSHEY_SIMPLEX
                strname = singledata['cls']
                strscore = singledata['score']
                #print (type(strscore))
                print (strscore)
                cv2.putText(img, strname + str(strscore) + '(' + str(xmax - xmin) + ',' + str(ymax - ymin) + ')', (xmin,ymin-10), font, 1,(0,0,255),2)
            print(os.path.join(imagepath_out,file))
            cv2.imwrite(os.path.join(imagepath_out,file), img)
end = time.time() - start
print end

#plot
#imagepath = '/data/ligang/detectron/Detectron-master/restful/vis/806_180507070134.jpg'
#img = cv2.imread(imagepath)
#cv2.rectangle(img, (136,63), (765,474),3)
#cv2.rectangle(img, (130,50), (537,239),3)
#cv2.imwrite('./001_new.jpg', img)
'''
################################################################
############################# curl #############################
curl -X POST 'http://192.168.200.213:9527/user' -d '{"data":"/opt/ligang/detectron/Detectron-master/restful/vis/180523_0006_6000.jpg"}' -H 'Content-Type: application/json'


curl -X POST 'http://192.168.200.213:9527/user' -d '{"data":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526895699811&di=5ce6acbcfe8f1d93fe65d3ae8eb3287d&imgtype=0&src=http%3A%2F%2Fimg1.fblife.com%2Fattachments1%2Fday_130616%2F20130616_e4c0b7ad123ca263d1fcCnkYLFk97ynn.jpg.thumb.jpg"}' -H 'Content-Type: application/json'
'''