#!/usr/bin/python3
# https://www.helywin.com/posts/20240108062631/#%e8%87%aa%e5%8a%a8%e8%bd%ac%e6%8d%a2%e5%b7%a5%e5%85%b7
# this script is used to initially replace the contents of the code with the ros2 writeup

import re
import sys

# create a list of all find and replace regular expression pairs
cpp_regex = [
    (r'\b(\w*_msgs)\:\:(?!msg)(\w{1,})\b', r'\1::msg::\2'),
    (r'\bconst (\w*_msgs\:\:msg\:\:\w*?)(::)?ConstPtr\s*&\s*(\w*)', r'\1::ConstSharedPtr \3'),
    (r'(\w*\-\>header\.stamp)\.toSec\(\)', r'rclcpp::Time(\1).seconds()'),
    (r'ros\:\:Time\(\)\.fromSec\((laserCloudTime)\)', r'rclcpp::Time(\1).seconds()'),
    (r'ros\:\:Time ', r'rclcpp::Time '),
    (r'ROS_(\w+)\(((?:.|\n)*?)\);', r'RCLCPP_\1(node->get_logger(), \2);'),
    ('<time.h>', '<ctime>'),
    ('<math.h>', '<cmath>'),
    ('<stdio.h>', '<cstdio>'),
    ('<stdlib.h>', '<cstdlib>'),
    ('<ros/ros.h>', '<rclcpp/rclcpp.hpp>'),
    ('<std_msgs/Bool.h>', '<std_msgs/msg/bool.hpp>'),
    ('<std_msgs/Int32.h>', '<std_msgs/msg/int32.hpp>'),
    ('<std_msgs/UInt32.h>', '<std_msgs/msg/uint32.hpp>'),
    ('<std_msgs/String.h>', '<std_msgs/msg/string.hpp>'),
    ('<std_msgs/Int32MultiArray.h>', '<std_msgs/msg/int32_multi_array.hpp>'),
    ('<std_msgs/Float32MultiArray.h>', '<std_msgs/msg/float32_multi_array.hpp>'),
    ('<std_msgs/ColorRGBA.h>', '<std_msgs/msg/color_rgba.hpp>'),
    ('<nav_msgs/Path.h>', '<nav_msgs/msg/path.hpp>'),
    ('<nav_msgs/Odometry.h>', '<nav_msgs/msg/odometry.hpp>'),
    ('<geometry_msgs/Pose.h>', '<geometry_msgs/msg/pose.hpp>'),
    ('<geometry_msgs/Point.h>', '<geometry_msgs/msg/point.hpp>'),
    ('<geometry_msgs/Polygon.h>', '<geometry_msgs/msg/polygon.hpp>'),
    ('<geometry_msgs/PoseStamped.h>', '<geometry_msgs/msg/pose_stamped.hpp>'),
    ('<geometry_msgs/PointStamped.h>', '<geometry_msgs/msg/point_stamped.hpp>'),
    ('<geometry_msgs/PolygonStamped.h>', '<geometry_msgs/msg/polygon_stamped.hpp>'),
    ('<sensor_msgs/PointCloud2.h>', '<sensor_msgs/msg/point_cloud2.hpp>'),
    ('<sensor_msgs/Joy.h>', '<sensor_msgs/msg/joy.hpp>'),
    ('<visualization_msgs/Marker.h>', '<visualization_msgs/msg/marker.hpp>'),
    ('<tf/transform_datatypes.h>', '<tf2/transform_datatypes.h>'),
    ('<tf/transform_broadcaster.h>', '<tf2_ros/transform_broadcaster.h>'),
    ('tf::TransformBroadcaster', 'tf2_ros::TransformBroadcaster'),
    ('tf::Matrix3x3', 'tf2::Matrix3x3'),
    ('ros::Publisher ', 'rclcpp::Publisher<>::SharedPtr '),
    ('ros::Subscriber ', 'rclcpp::Subscription<>::SharedPtr '),
    ('tf::Vector3', 'tf2::Vector3'),
    ('tf::Quaternion', 'tf2::Quaternion'),
    ('ros::NodeHandle nh;', 'rclcpp::Node node();'),
    ('ros::Rate', 'rclcpp::Rate'),
    ('ros::ok', 'rclcpp::ok'),
    ('ros::init', 'rclcpp::init'),
    ('ros::spin', 'rclcpp::spin'),
    ('ros::Timer ', 'rclcpp::TimerBase::SharedPtr '),
    ('tf2::StampedTransform', 'geometry_msgs::msg::TransformStamped'),
    ('\.publish', '->publish'),
    ('boost::bind', 'std::bind'),
]

cmake_regex = [
    (r'cmake_minimum_required\(VERSION (.*)\)', r'cmake_minimum_required(VERSION 3.5)'),
]

# launch
launch_regex = [
    # type to exec
    (r'(\<node.*?)type=(.*/?\>)', r'\1exec=\2'),
    # remove required from node
    (r'(\<node.*?) required\=\"\w*?\"(.*/?\>)', r'\1\2'),
    # remove the type from param
    (r'(\<param.*?) type=\"\w*?\"(.*/?\>)', r'\1\2'),
    (r'\$\(find ', '$(find-pkg-share '),
    (r'\bns\b', 'namespace'),
    (r'\$\(arg', '$(var'),
    ('pkg\=\"rviz\"', 'pkg=\"rviz2\"'),
    ('name\=\"rviz\"', 'name=\"rviz2\"'),
    ('exec\=\"rviz\"', 'exec=\"rviz2\"'),
]

if __name__ == '__main__':
    # if argc 2 then run the test code otherwise read the argv 1 file and replace the file contents
    open_file = len(sys.argv) > 1

    if open_file:
        text = open(sys.argv[1]).read()
    else:
        text = "const sensor_msgs::PointCloud2ConstPtr& laserCloud2"

    regex_pairs = []
    # selecting regular expressions based on file suffixes
    if open_file and (sys.argv[1].endswith('.cpp') or sys.argv[1].endswith('.h') or sys.argv[1].endswith('.hpp')):
        print('cpp file')
        regex_pairs = cpp_regex
    elif open_file and (sys.argv[1].endswith('.cmake') or sys.argv[1].endswith('CMakeLists.txt')):
        print('cmake file')
        regex_pairs = cmake_regex
    elif open_file and sys.argv[1].endswith('.launch'):
        print('launch file')
        regex_pairs = launch_regex

    for find, replace in regex_pairs:
        text = re.sub(find, replace, text)

    # save
    if open_file:
        with open(sys.argv[1], 'w') as f:
            f.write(text)
    else:
        print(text)