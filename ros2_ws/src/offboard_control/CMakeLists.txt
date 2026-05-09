cmake_minimum_required(VERSION 3.8)
project(offboard_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)

include_directories(include)

add_executable(offboard_control_node
  src/main.cpp
  src/offboard_control.cpp
)

ament_target_dependencies(offboard_control_node
  rclcpp
  px4_msgs
)

install(TARGETS offboard_control_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()