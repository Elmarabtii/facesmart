import cv2
import facesmart
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-8a4e1-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-8a4e1.appspot.com"
})

# Import student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

# Upload images to Google Cloud Storage
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentId = os.path.splitext(path)[0]
    studentIds.append(studentId)

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

# Function to find face encodings in images
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started ...")

# Encode faces in images
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encoding data to a pickle file
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
