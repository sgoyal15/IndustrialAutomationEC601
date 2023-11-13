import cv2
import numpy as np
cap=cv2.VideoCapture(0)
skip=0
face_data=[]
face_cascade=cv2.CascadeClassifier('/Users/shivam_goyal/Documents/Python/Haarcascade/haarcascade_frontalface_alt.xml')
dataset_path='/Users/shivam_goyal/Desktop/ECE601/Sprint3/faceDataCollect/'
file_name=input("Confirm the name of the person: ")
while True:
	ret,frame=cap.read()

	if ret== False:
		continue
	gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	#cv2.imshow("Frame",frame)

	faces=face_cascade.detectMultiScale(frame,1.3,5)
	if len(faces)==0:
		continue
	#print(faces)           
	faces=sorted(faces,key= lambda f:f[2]*f[3])
# Pick the last face cause it will be the largest
	for face in faces[-1:]:
		x,y,w,h=face
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)

# Extract ( Crop out the required face ): Region of interest
		offset=10
		# next is slicing of frame-> in this frame the first axis is y and 2nd is x i.e. frame[y,x]
		face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section=cv2.resize(face_section,(100,100))

		skip+=1
		if skip%10==0:
			face_data.append(face_section)
			print(len(face_data))
		

	cv2.imshow("Frame",frame)
	cv2.imshow("Face section",face_section)



	key_pressed=cv2.waitKey(1) & 0xFF
	if key_pressed==ord('q'):
		break
	# convert face list array into a numpy array
face_data=np.asarray(face_data)
face_data=face_data.reshape((face_data.shape[0],-1))
print(face_data.shape)

# save the numpy array into a file system
# np.save(dataset_path+file_name+'.npy',face_data)
np.save(dataset_path+file_name+'.npy',face_data)
print('data saved succesfully'+dataset_path+file_name+'.npy')

cap.release()
cv2.destroyAllWindows()


