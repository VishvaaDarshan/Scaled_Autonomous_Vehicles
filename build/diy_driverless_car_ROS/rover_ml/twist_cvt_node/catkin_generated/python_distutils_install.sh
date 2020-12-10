#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS/rover_ml/twist_cvt_node"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/prajval/end_to_end_learning/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/prajval/end_to_end_learning/install/lib/python2.7/dist-packages:/home/prajval/end_to_end_learning/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/prajval/end_to_end_learning/build" \
    "/usr/bin/python2" \
    "/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS/rover_ml/twist_cvt_node/setup.py" \
     \
    build --build-base "/home/prajval/end_to_end_learning/build/diy_driverless_car_ROS/rover_ml/twist_cvt_node" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/prajval/end_to_end_learning/install" --install-scripts="/home/prajval/end_to_end_learning/install/bin"
