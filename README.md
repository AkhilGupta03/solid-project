# Attendance using face recognition 

### Project flow & explaination
- After you run the project you have to register your face so that system can identify you, so click on register employee
- After you click a small window will pop up in that you have to enter your employee ID and name and then click on `Take Image` button
- After clicking `Take Image` button A camera window will pop up and it will detect your Face and take upto 50 Images(you can change the number of Image it can take) and stored in the folder named `TrainingImage`. more you give the image to system, the better it will perform while recognising the face.
- Then you have to click on `Train Image` button, It will train the model and convert all the Image into numeric format so that computer can understand. we are training the image so that next time when we will show the same face to the computer it will easily identify the face.
- It will take some time(depends on you system).
- After training model click on `Automatic Attendance` ,you have to choose the department name and then it can fill in-time and out-time attendace by your face using our trained model.
- it will create `.csv` file for every department you choose and seperate every `.csv` file accoriding the deaprtment.
- You can view the attendance after clicking `View Attendance` button. It will show record in tabular format.
