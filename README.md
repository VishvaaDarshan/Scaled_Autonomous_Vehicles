# Scaled Autonomy (AuE8930)
This repository contains final project done in the course, AuE8930 - Scaled Autonomy during the Fall Semester 2020 at Clemson Univerity - International Center for Automotive Research.





## Team Members
1. Prajval Vaskar pvaskar@g.clemson.edu
2. Ajith Kumar Challa ajithc@g.clemson.edu
3. Shaurya Panthri spanthr@clmeson.edu 
4. Kexuan Zhai kzhai@clemson.edu

## Installation Steps and training procedure.

1. Clone the repository and build the package. The repository contains the required dependancy so there should not be any error while building.
2. Download the conde world required from [here](https://s3-us-west-2.amazonaws.com/selbystorage/wp-content/uploads/2017/July/conde_world.zip). The model should be saved in default gazebo world directory ~/.gazebo/models.
3. To launch the simulator use, "roslaunch rover_gazebo rc_dbw_walker.launch world_name:=conde_world". Initially the map is relatively small compared to the MIT car. To scale the map, make changes in sdf file for conde world.
4. Once the simulation is loaded, we will begin recording data. The 'record_training.sh' (can be found in utils) script is used to record the topics that are required for the training datasets.
5. Once we’ve collected the training data, we need to organize and process it. We want to extract the camera data and steering data from the ROS bag and save it in a format that is easier to manipulate. We will save the camera images as JPG files with unique filenames based on the timestamp they were recorded. We also extract the steering commands which are stored in a CSV file. Each row in the CSV file lists the image filename as well as the steering and throttle values associated with that image.
6. To execute the transformation, we will use the 'rosbag_to_csv.py'(found in utils).
7. To run the script sucessfully, check the path of input data and output data folder.
8. After collecting the data and converting the data into images and csv files, model trainig should be done. 
9. To train the model (NVIDIA CNN model for steering and speed prediction), run the python script 'train_model_CNN.py' which can be found in behavior cloning folder. 
10. After training the network, weights will be saved in weights folder if all paths and othe steps are done carefully.
11. To deploy the model, launch the simulator and run the python sctipt 'drive_model_vel_CNN.py'
 
 
In case of package dependency issue, use the following links to clone the required packages.
1. [Yujin_ocs](https://github.com/yujinrobot/yujin_ocs/tree/devel/yocs_cmd_vel_mux)
2. [ecl_exeptions](https://github.com/stonier/ecl_core/tree/devel/ecl_exceptions)
3. [Yujin_msgs](https://github.com/yujinrobot/yocs_msgs)

## Results:
1. Interpretating the results of neural networks:
Overfitting: 𝑉𝑎𝑙𝑖𝑑𝑎𝑡𝑖𝑜𝑛 𝑙𝑜𝑠𝑠≫𝑇𝑟𝑎𝑖𝑛𝑖𝑛𝑔 𝑙𝑜𝑠𝑠
Underfitting: 𝑉𝑎𝑙𝑖𝑑𝑎𝑡𝑖𝑜𝑛 𝑙𝑜𝑠𝑠≪𝑇𝑟𝑎𝑖𝑛𝑖𝑛𝑔 𝑙𝑜𝑠𝑠

2. Techniques to improve the accuracy of the model:

Collecting more data for training: Collecting more data always does not yield better results if the images or not shuffled or balance in the data is not there.
Solution – Add dropout layers and balance the dataset

3. Splitting training data set and validation data set
a. General split is 80:20
b. If validation dataset is too less, overfitting is possible.
c. Iterated with 75:25
d. No performance difference is observed


4. Using different activation functions
a. Tanh: Tanh activation yielded only the extremes of steering values which are -0.45 and 0.45 in all cases.Due to the vanishing gradient problem when using tanh activation function, the initial layers might not learn anything when the backward pass happens which could be one of the reasons for the extreme values.

b. ReLU activation function:
Can be considered as Linear function Range – [0,inf) No saturation. There wouldn’t be vanishing gradient problem 

5. Normalization of images, speed, and steering values:
Allows the neural network is not biased towards activations which have higher values.
Improved the rate of convergence of the loss function and thus reduces the number of epochs significantly


6. Tuning hyperparameters
a. Dropout Layers:
-Overfitting because there are no dropout layers in the first plot.
-𝑉𝑎𝑙𝑖𝑑𝑎𝑡𝑖𝑜𝑛 𝑙𝑜𝑠𝑠≫𝑇𝑟𝑎𝑖𝑛𝑖𝑛𝑔 𝑙𝑜𝑠𝑠
Dropout layers of 0.3, 0.3, 0.2 and 0.2 made the model to fit just right.
b.Batch size:
-Number of training examples used in the estimate of the error gradient
-Tried with batch sizes: 32 and 50 
-No substantial difference in performance and loss
c. Number of epochs
- Significant effect on accuracy of the model
- Directly proportional to accuracy
- Accuracy gets saturate at a certain number of epochs
d. Input normalization reduced the number of epochs needed by 50%
e. Cropping the top half of the image reduced the time for each epoch by 25% which is from 120 seconds to 90 seconds on CPU.

7. Normalization of images, speed, and steering values

## Training and Data
Teleoperation

![_](https://github.com/Praj390/Scaled_Autonomous_Vehicles/blob/main/Images/5.gif)

## Performace
1. Initial Performance

![_](https://github.com/Praj390/Scaled_Autonomous_Vehicles/blob/main/Images/1.gif)


2. Training for features. Line Following

![_](https://github.com/Praj390/Scaled_Autonomous_Vehicles/blob/main/Images/23.gif)

3. Steering Prediction with uniform Velocity 

![_](https://github.com/Praj390/Scaled_Autonomous_Vehicles/blob/main/Images/3.gif)

4. Behavior cloning using Deep CNN (Steering and Speed Prediction)

![_](https://github.com/Praj390/Scaled_Autonomous_Vehicles/blob/main/Images/4.gif)


## Conclusion
Using ReLU activation function 
Normalization of the inputs reduced epoch numbers by 50%
Training on more data always does not yield generalized output.
Cropping the images which has unwanted data decreased the training duration by 40%.
Data augmentation by flipping increased the data size and contributed for more generalization.

## Future Scope
1.The performance might be still improved using the following techniques:
2. Weight regularization which reduces overfitting
3. K-cross validation while training which improves generalization.
4. Implementation of advanced neural networks which are GRU and LSTM and compare the performance of CNN and RNNs is also one future direction.
5. Hardware Implementation
