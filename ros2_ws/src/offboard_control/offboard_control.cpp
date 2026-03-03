//
// Created by sandhm1 on 3/2/26.
//

#include "offboard_control.h"
#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_status.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>

class OffboardControl : public rclcpp::Node {
    public:
        OffboardControl() : rclcpp::Node("offboard_control") {
            vehicle_command_pub = this->create_publisher<px4_msgs::msg::VehicleCommand>(
            "/fmu/in/vehicle_command",
            10
            );

            offboard_control_pub = this->create_publisher<px4_msgs::msg::VehicleCommand>(

            )
        }



    private:
        rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub;
};

// msg.position = true;
// msg.velocity = false;
// msg.acceleration = false;
// msg.attitude = false;
// msg.body_rate = false;