# Scaled Autonomy (AuE8930)
This repository contains final project done in the course, AuE8930 - Scaled Autonomy during the Fall Semester 2020 at Clemson Univerity - International Center for Automotive Research.

## Installation Steps and training procedure.

1. Clone the repository and build the package. The repository contains the required dependancy so there should not be any error while building.
2. Download the conda world required from [here](https://s3-us-west-2.amazonaws.com/selbystorage/wp-content/uploads/2017/July/conde_world.zip). The model should be saved in default gazebo world directory ~/.gazebo/models.
3. To launch the simulator use, "roslaunch rover_gazebo rc_dbw_walker.launch world_name:=conde_world". Initially the map is relatively low compared to the MIT car. To scale the map, make changes in sdf file for conde world.
4. Once the simulation is loaded, we will begin recording data. The 'record_training.sh' (can be found in utils) script is used to record the topics required for the training datasets.
5. Once we’ve collected the training data, we need to organize and process it. We want to extract the camera data and steering data from the ROS bag and save it in a format that is easier to manipulate. We will save the camera images as JPG files with unique filenames based on the timestamp they were recorded. We also extract the steering commands which are stored in a CSV file. Each row in the CSV file lists the image filename as well as the steering and throttle values associated with that image.
6. To execute the transformation, we will use the 'rosbag_to_csv.py'(found in utils).
7. To run the script sucessfully, check the path of input data and output data folder.
8. After collecting the data and converting the data into images and csv files, model trainig should be done. 
9. To train the model (NVIDIA CNN model for steering and speed prediction), run the python script 'train_model_CNN.py' which can be found in behavior cloning folder. 
10. After training the network, weights will be saved in weights folder if all paths and othe steps are done carefully.
11. To deploy the model, launch the simulator and run the python sctipt 'drive_model_vel_CNN.py'
 
In case of package dependacny issue, use the following links to clone the required packages.
1. [Yujin_ocs](https://github.com/yujinrobot/yujin_ocs/tree/devel/yocs_cmd_vel_mux)
2. [ecl_exeptions](https://github.com/stonier/ecl_core/tree/devel/ecl_exceptions)