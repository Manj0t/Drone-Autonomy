//
// Created by sandhm1 on 3/2/26.
//

#ifndef ROS2_WS_OFFBOARD_CONTROL_H
#define ROS2_WS_OFFBOARD_CONTROL_H


#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

// rclcpp::Node, is a ROS2 Node. Comes from #include <rclcpp/rclcpp.hpp>
class OffboardControl : public rclcpp::Node
{
public:
    OffboardControl();

private:
    void timer_callback();

    // rclcpp::Publisher<MsgT> Templated type
    rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub_;
    rclcpp::Publisher<px4_msgs::msg::OffboardControlMode>::SharedPtr offboard_control_mode_pub_;
    rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_setpoint_pub_;

    // Holds the timer. If not stored, it can get destroyed and stop firing
    rclcpp::TimerBase::SharedPtr timer_;

    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr map_sub_;
    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr pose_sub_;

    void map_callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg);
    void pose_callback(const geometry_msgs::msg::PoseStamped::SharedPtr msg);

    // Store current state
    geometry_msgs::msg::Point current_pose_;
    geometry_msgs::msg::Point current_goal_;
    bool has_goal_ = false;
};


#endif //ROS2_WS_OFFBOARD_CONTROL_H