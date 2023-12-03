import cv2
import numpy as np
import os
from config import config, get_worker_config, hex_colors

def dist(x1,x2):
    return np.sqrt(sum((x2-x1)**2))

def knn(X,Y,query_point,k=5):
    vals=[]
    m=X.shape[0]
    for i in range(m):
        d=dist(query_point,X[i])
        vals.append((d,Y[i]))
    
    vals=sorted(vals)
    vals=vals[:k]
    vals=np.array(vals)
    new_vals=np.unique(vals[:,1],return_counts=True)
    print(new_vals)
    index=new_vals[1].argmax()
    pred=new_vals[0][index]
    return pred

cap=cv2.VideoCapture(0)
skip=0
dataset_path='//Users/shivam_goyal/Desktop/ECE601/Sprint3/faceDataCollect/'
face_data=[] # X data
labels=[]	# Y data
class_id=0 # labels for the given file
names={} #Mapping between id and name

# DATA PREPERATION

for fx in os.listdir(dataset_path):
	if fx.endswith('.npy'):
		# Create a mapping 
		names[class_id]=fx[:-4]
		data_item=np.load(dataset_path+fx)
		face_data.append(data_item)

		# Labels for the class
		target=class_id*np.ones((data_item.shape[0],))
		class_id+=1;
		labels.append(target)
face_dataset=np.concatenate(face_data,axis=0)
face_labels=np.concatenate(labels,axis=0).reshape((-1,1))

trainset=np.concatenate((face_dataset,face_labels),axis=1)

# Testing
face_cascade=cv2.CascadeClassifier('/Users/shivam_goyal/Documents/Python/Haarcascade/haarcascade_frontalface_alt.xml')
while True:
	ret,frame=cap.read()
	if ret==False:
		continue

	faces=face_cascade.detectMultiScale(frame,1.3,5)
	if(len(faces)==0):
		continue
	for face in faces[-1:]:
		x,y,w,h=face
		offset=10
		face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section=cv2.resize(face_section,(100,100))

		# Predicted Label
		#out=knn(trainset,face_section.flatten())
		out=knn(face_dataset,face_labels,face_section.flatten())

		# Display on the screen the name and the rectangle around it
		pred_name=names[int(out)]
		
		cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv2.LINE_AA)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
	cv2.imshow("Faces",frame)

	worker_names = [worker["name"] for worker in config.get("workers")]
	key_pressed=cv2.waitKey(1) & 0xFF

	if pred_name in worker_names or key_pressed==ord('q'):
		break

	
	# if key_pressed==ord('q'):
	# 	break
cap.release()
cv2.destroyAllWindows()

