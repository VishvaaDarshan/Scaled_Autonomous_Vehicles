execute_process(COMMAND "/home/prajval/end_to_end_learning/build/diy_driverless_car_ROS/rover_webcam/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/prajval/end_to_end_learning/build/diy_driverless_car_ROS/rover_webcam/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
