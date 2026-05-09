#include <rclcpp/rclcpp.hpp>
#include "offboard_control/offboard_control.h"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);                        // start ROS 2

  auto node = std::make_shared<OffboardControl>(); 

  rclcpp::spin(node);                              // event loop: runs timer_callback() every 50ms

  rclcpp::shutdown();                              // clean shutdown
  return 0;
}