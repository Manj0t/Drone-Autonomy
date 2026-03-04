//
// Created by sandhm1 on 3/2/26.
//

#include "offboard_control/offboard_control.h"

#include <chrono>
#include <functional>

OffboardControl::OffboardControl() : rclcpp::Node("offboard_control") {
    // For sending vehicle commands (arm, disarm, switch ot offboard mode, land, etc.)
    vehicle_command_pub_ = this->create_publisher<px4_msgs::msg::VehicleCommand>(
        "/fmu/in/vehicle_command", // Topic messages are sent to
        10                         // Keep up to 10 outgoing messages in a buffer if the subscriber (bridge) can't keep up. Queue based
    );

    // Selecting the type of control being sent (velocity, acceleration, position, altitude, body rates, etc)
    offboard_control_mode_pub_ = this->create_publisher<px4_msgs::msg::OffboardControlMode>(
        "/fmu/in/offboard_control_mode",
        10
    );
    
    // Setting control value (How much for velocity, acc, etc.). While in Offboard.
    trajectory_setpoint_pub_ = this->create_publisher<px4_msgs::msg::TrajectorySetpoint>(
        "/fmu/in/trajectory_setpoint",
        10
    );

    // Create a timer based on real ("wall") time
    // Comes from rclcpp
    timer_ = this->create_wall_timer(
        std::chrono::milliseconds(50),  // 20Hz = 50ms. C++ standard library <chrono>
        std::bind(&OffboardControl::timer_callback, this)  //<functional>
    ); // Call this->timer_callback() every 50ms
}

void OffboardControl::timer_callback() {
    // Create OffboardCtonrlMode var and set default vals (false)
    px4_msgs::msg::OffboardControlMode mode{};
    mode.position = true; // Will be providing pos info

    px4_msgs::msg::TrajectorySetpoint setpoint{};
    // x = North, y = East, z = Down
    setpoint.position = {0.0, 0.0, -5.0}; // hover 5m up

    // .publish() hands message to ROS middleware, which sends it to anyone subscribed to the topic. (PX4 bridge)
    offboard_control_mode_pub_->publish(mode);
    trajectory_setpoint_pub_->publish(setpoint);
}

// msg.position = true;
// msg.velocity = false;
// msg.acceleration = false;
// msg.attitude = false;
// msg.body_rate = false;
