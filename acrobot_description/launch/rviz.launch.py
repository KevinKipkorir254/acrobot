import os
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

package_name = "acrobot_description"
urdf_file_name = "robot.urdf"

def generate_launch_description():

    urdf_file = os.path.join(get_package_share_directory(package_name), "acrobot", urdf_file_name)
    rviz_config = os.path.join(get_package_share_directory(package_name), "rviz", "acrobot.rviz")

    with open(urdf_file, 'r') as infp:
        robot_descr = infp.read()

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description":robot_descr}]
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments = ["-d", rviz_config],
    )

    joint_state_publisher_gui = Node(
        package =  "joint_state_publisher_gui",
        executable = "joint_state_publisher_gui",
        output = "screen",
    )

    
    return LaunchDescription(
        [
            rsp, 
            rviz2_node,
            joint_state_publisher_gui,
        ]
    )


