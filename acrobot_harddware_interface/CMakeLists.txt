cmake_minimum_required(VERSION 3.8)
project(acrobot_harddware_interface)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(PkgConfig REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
# Add REQUIRED flag to ensure LibSerial is found
pkg_check_modules(SERIAL REQUIRED libserial)

# Add the plugin XML to the install
install(FILES
    acrobot_harddware_interface.xml
    DESTINATION share/${PROJECT_NAME}/
)

add_library(
  ${PROJECT_NAME} SHARED
  src/hardware_interface.cpp
  src/stop_and_wait.cpp
)

target_include_directories(
  ${PROJECT_NAME} PRIVATE
  include
  ${SERIAL_INCLUDE_DIRS}  # Changed from quoted to regular variable
)

# Use SERIAL_LIBRARIES instead of SERIAL_LDFLAGS
target_link_libraries(
  ${PROJECT_NAME}
  ${SERIAL_LIBRARIES}  # Changed from SERIAL_LDFLAGS to SERIAL_LIBRARIES
)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp_lifecycle
  rclcpp
  pluginlib
  hardware_interface
)

pluginlib_export_plugin_description_file(hardware_interface acrobot_harddware_interface.xml)

ament_python_install_package(${PROJECT_NAME})

install(
  TARGETS ${PROJECT_NAME}
  DESTINATION lib
)

install(
  DIRECTORY include
  DESTINATION include
)

# Fixed syntax for include directories export (removed parentheses)
ament_export_include_directories(
  include
)

ament_export_libraries(
  ${PROJECT_NAME}
)

ament_export_dependencies(
  rclcpp_lifecycle
  rclcpp
  pluginlib
  hardware_interface
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
