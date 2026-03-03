#!/bin/bash
#
# URDF Validation Script for Simple Humanoid
#
# This script demonstrates how to validate URDF files using
# the check_urdf tool from ROS 2.
#
# Usage:
#   ./check_urdf_example.sh [path_to_urdf_file]
#
# Example:
#   ./check_urdf_example.sh simple_humanoid.urdf
#

# Set URDF file path (use argument or default)
URDF_FILE="${1:-simple_humanoid.urdf}"

echo "=================================="
echo "URDF Validation Script"
echo "=================================="
echo ""

# Check if file exists
if [ ! -f "$URDF_FILE" ]; then
    echo "Error: URDF file '$URDF_FILE' not found!"
    echo ""
    echo "Usage: $0 [urdf_file]"
    echo "Example: $0 simple_humanoid.urdf"
    exit 1
fi

echo "Checking URDF file: $URDF_FILE"
echo ""

# Check if check_urdf command exists
if ! command -v check_urdf &> /dev/null; then
    echo "Error: check_urdf command not found!"
    echo ""
    echo "Make sure ROS 2 is installed and sourced:"
    echo "  source /opt/ros/humble/setup.bash"
    echo ""
    echo "Then install urdf_tools:"
    echo "  sudo apt install ros-humble-urdfdom-tools"
    exit 1
fi

# Run check_urdf
echo "Running check_urdf..."
echo "--------------------"
check_urdf "$URDF_FILE"
RESULT=$?

echo ""
echo "--------------------"

# Check result
if [ $RESULT -eq 0 ]; then
    echo "✓ URDF validation PASSED"
    echo ""
    echo "Next steps:"
    echo "  1. Visualize in RViz: ros2 run rviz2 rviz2"
    echo "  2. Load in Gazebo: ros2 run gazebo_ros spawn_entity.py -file $URDF_FILE"
    exit 0
else
    echo "✗ URDF validation FAILED"
    echo ""
    echo "Common errors:"
    echo "  - Malformed XML (unclosed tags)"
    echo "  - Invalid joint hierarchy (loops)"
    echo "  - Missing required attributes"
    exit 1
fi
