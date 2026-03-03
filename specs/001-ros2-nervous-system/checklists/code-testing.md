# Code Testing Checklist: Module 1 - ROS 2 Examples

**Purpose**: Verify all code examples run successfully in ROS 2 Humble environment
**Created**: 2026-03-03
**Feature**: Module 1 - The Robotic Nervous System (ROS 2)

## Pre-Testing Setup

- [ ] ROS 2 Humble installed and sourced (`source /opt/ros/humble/setup.bash`)
- [ ] Gazebo Fortress installed and functional
- [ ] Python 3.8+ available (`python3 --version`)
- [ ] rclpy importable (`python3 -c "import rclpy"`)
- [ ] Code examples copied to workspace (`~/ros2_ws/src/examples/`)
- [ ] Examples made executable (`chmod +x *.py`)

## Chapter 1: ROS 2 Fundamentals Examples

### hello_world_node.py

**File**: `examples/hello_world_node.py`

- [ ] **Test 1.1**: Script executes without errors
  ```bash
  python3 hello_world_node.py
  ```
  Expected: "Hello, ROS 2! This is my first humanoid robot node." message

- [ ] **Test 1.2**: Node initializes successfully
  Expected: No errors during `rclpy.init()`

- [ ] **Test 1.3**: Node shuts down cleanly
  Expected: "Node shutdown complete" message

- [ ] **Test 1.4**: Comments explain ROS 2 concepts
  Verify: All ROS 2-specific lines have explanatory comments

- [ ] **Test 1.5**: Code follows PEP 8
  Test: `pylint hello_world_node.py` or `flake8 hello_world_node.py`
  Expected: 0 errors, warnings acceptable if documented

### simple_talker.py

**File**: `examples/simple_talker.py`

- [ ] **Test 2.1**: Publisher node starts successfully
  ```bash
  python3 simple_talker.py
  ```
  Expected: "Humanoid Status Publisher started" message

- [ ] **Test 2.2**: Messages published periodically
  Expected: "Publishing: Humanoid status message #N" every 1 second

- [ ] **Test 2.3**: Topic appears in active topics
  ```bash
  # In another terminal
  ros2 topic list
  ```
  Expected: `/humanoid/status` in the list

- [ ] **Test 2.4**: Topic type is correct
  ```bash
  ros2 topic info /humanoid/status
  ```
  Expected: `TypeName: std_msgs/msg/String`

- [ ] **Test 2.5**: Messages can be echoed
  ```bash
  ros2 topic echo /humanoid/status
  ```
  Expected: Messages displayed in real-time

- [ ] **Test 2.6**: QoS settings are correct
  Expected: Queue size of 10, default QoS

- [ ] **Test 2.7**: Node handles Ctrl+C gracefully
  Expected: "Keyboard interrupt, shutting down..." message

- [ ] **Test 2.8**: PEP 8 compliance verified

### simple_listener.py

**File**: `examples/simple_listener.py`

- [ ] **Test 3.1**: Subscriber node starts successfully
  ```bash
  python3 simple_listener.py
  ```
  Expected: "Humanoid Status Subscriber started" message

- [ ] **Test 3.2**: Receives messages from talker
  Expected: "Received: Humanoid status message #N" messages

- [ ] **Test 3.3**: Callback processes messages correctly
  Expected: No errors in callback function

- [ ] **Test 3.4**: Topic subscription is correct
  ```bash
  ros2 topic info /humanoid/status
  ```
  Expected: Subscription count includes this node

- [ ] **Test 3.5**: Multiple scenarios tested
  - [ ] Talker starts before listener
  - [ ] Listener starts before talker
  - [ ] Multiple listeners (run listener twice)

- [ ] **Test 3.6**: Error handling in callback
  Verify: Callback logs warnings for error conditions

- [ ] **Test 3.7**: Node handles Ctrl+C gracefully

- [ ] **Test 3.8**: PEP 8 compliance verified

### simple_service.py

**File**: `examples/simple_service.py`

- [ ] **Test 4.1**: Service server starts successfully
  ```bash
  # Terminal 1
  python3 simple_service.py
  ```
  Expected: "Calibration Service started" message

- [ ] **Test 4.2**: Service appears in active services
  ```bash
  ros2 service list
  ```
  Expected: `/humanoid/calibrate_joint` in the list

- [ ] **Test 4.3**: Service type is correct
  ```bash
  ros2 service type /humanoid/calibrate_joint
  ```
  Expected: `example_interfaces/srv/AddTwoInts`

- [ ] **Test 4.4**: Client can call service
  Expected: No "Service not available" errors

- [ ] **Test 4.5**: Service processes request correctly
  Expected: `result.sum = request.a + request.b`

- [ ] **Test 4.6**: Response returned to client
  Expected: Client receives result

- [ ] **Test 4.7**: Service handles multiple requests
  Test: Send multiple requests sequentially
  Expected: All requests processed correctly

- [ ] **Test 4.8**: Client handles service unavailability
  Test: Run client without server
  Expected: "Service not available!" error message

- [ ] **Test 4.9**: PEP 8 compliance verified

## Integration Testing

### Talker-Listener Integration

- [ ] **Test I.1**: Talker and listener communicate
  ```bash
  # Terminal 1: Start talker
  python3 simple_talker.py

  # Terminal 2: Start listener
  python3 simple_listener.py
  ```
  Expected: Listener receives all messages from talker

- [ ] **Test I.2**: Multiple subscribers scenario
  Expected: All listeners receive messages

- [ ] **Test I.3**: Message order preserved
  Expected: Messages arrive in sequence (#1, #2, #3, ...)

### Service Client-Server Integration

- [ ] **Test I.4**: Server and client communicate
  Expected: Requests and responses match

- [ ] **Test I.5**: Multiple clients scenario
  Test: Run multiple client instances
  Expected: All clients receive responses

## Error Handling Testing

### ROS 2 Environment Errors

- [ ] **Test E.1**: Handles missing ROS 2 setup
  Test: Run without sourcing `/opt/ros/humble/setup.bash`
  Expected: Clear error message about sourcing setup

- [ ] **Test E.2**: Handles node name conflicts
  Test: Run two instances of same node
  Expected: Appropriate error or naming conflict message

- [ ] **Test E.3**: Handles topic/Service not found
  Test: Subscribe to non-existent topic or call non-existent service
  Expected: Timeout or clear error message

### Code Robustness

- [ ] **Test E.4**: All examples handle KeyboardInterrupt
  Test: Press Ctrl+C in all examples
  Expected: Clean shutdown with "shutting down" message

- [ ] **Test E.5**: No resource leaks
  Test: Run examples multiple times
  Expected: No "port already in use" or resource errors

## Code Quality Verification

### PEP 8 Compliance

- [ ] **Test Q.1**: All examples pass pylint
  ```bash
  pylint *.py
  ```
  Expected: 0 errors, warnings documented if acceptable

- [ ] **Test Q.2**: All examples pass flake8
  ```bash
  flake8 *.py --max-line-length=100
  ```
  Expected: 0 errors

### Documentation

- [ ] **Test Q.3**: All examples have docstrings
  Verify: Each file has module-level docstring

- [ ] **Test Q.4**: All functions have docstrings
  Verify: Functions have clear docstrings explaining purpose

- [ ] **Test Q.5**: ROS 2 concepts explained in comments
  Verify: rclpy-specific lines have comments explaining why

### Humanoid Robot Context

- [ ] **Test Q.6**: All examples use humanoid robot scenarios
  Verify: No wheeled robot or manipulator-only references

- [ ] **Test Q.7**: Topic names follow humanoid conventions
  Verify: Topics like `/humanoid/status`, not `/robot/status`

## Performance Testing

- [ ] **Test P.1**: Node startup time acceptable
  Expected: Nodes start within 5 seconds

- [ ] **Test P.2**: Memory usage reasonable
  Test: Monitor with `top` or `htop`
  Expected: < 100 MB per node

- [ ] **Test P.3**: CPU usage minimal (idle)
  Expected: < 5% CPU when not processing

## Testing Environment Verification

- [ ] **Test V.1**: Clean ROS 2 environment test
  Test: Run in fresh terminal with only `source /opt/ros/humble/setup.bash`
  Expected: All examples work

- [ ] **Test V.2**: Ubuntu 22.04 compatibility
  Verify: Tested on Ubuntu 22.04 (or specified target OS)

- [ ] **Test V.3**: Python version compatibility
  Test: `python3 --version` shows 3.8+
  Expected: Examples run without syntax errors

## Chapter 3: URDF Examples

### simple_humanoid.urdf

**File**: `examples/simple_humanoid.urdf`

- [ ] **Test U.1**: URDF validates successfully with check_urdf
  ```bash
  check_urdf simple_humanoid.urdf
  ```
  Expected: "robot name is: simple_humanoid" and "Successfully Parsed XML"

- [ ] **Test U.2**: Root link identified correctly
  Expected: "root link: torso"

- [ ] **Test U.3**: Joint hierarchy is correct
  Expected: 5 joints listed (neck, left_shoulder, left_elbow, right_shoulder, right_elbow)

- [ ] **Test U.4**: No syntax errors
  Expected: No XML parsing errors or missing tag errors

- [ ] **Test U.5**: Tree structure verified
  Expected: No cycles in joint hierarchy

- [ ] **Test U.6**: All links have required properties
  Verify: Each link has visual, collision, and inertial tags

- [ ] **Test U.7**: All joints have required attributes
  Verify: Each joint has parent, child, origin, axis, and limit tags

- [ ] **Test U.8**: Joint limits are realistic
  Verify: lower < upper for all revolute joints

### check_urdf_example.sh

**File**: `examples/check_urdf_example.sh`

- [ ] **Test U.9**: Script executes without errors
  ```bash
  ./check_urdf_example.sh simple_humanoid.urdf
  ```
  Expected: Script runs and produces output

- [ ] **Test U.10**: Script validates URDF file
  Expected: Passes URDF validation and reports success

- [ ] **Test U.11**: Script handles missing file gracefully
  ```bash
  ./check_urdf_example.sh nonexistent.urdf
  ```
  Expected: Error message about file not found

- [ ] **Test U.12**: Script is executable
  Test: `ls -l check_urdf_example.sh`
  Expected: Executable permissions set

### URDF Visualization Testing

- [ ] **Test U.13**: URDF loads in RViz2
  ```bash
  ros2 run rviz2 rviz2
  # Add RobotModel display, set robot_description to URDF path
  ```
  Expected: Robot model appears with all links

- [ ] **Test U.14**: Robot structure is correct in RViz2
  Expected: Torso, head, arms visible and connected properly

- [ ] **Test U.15**: Joints can be manipulated in RViz2
  Expected: Sliders control joint positions within limits

- [ ] **Test U.16**: URDF spawns in Gazebo
  ```bash
  ros2 launch gazebo_ros gazebo.launch.py
  ros2 run gazebo_ros spawn_entity.py -entity simple_humanoid -file simple_humanoid.urdf
  ```
  Expected: Robot appears in simulation

- [ ] **Test U.17**: Physics simulation works correctly
  Expected: Robot falls to ground and stabilizes

- [ ] **Test U.18**: Joint limits enforced in Gazebo
  Expected: Joints stop at defined limits

### URDF Structure Verification

- [ ] **Test U.19**: Correct number of links
  Expected: 6 links (torso, head, left_upper_arm, left_forearm, right_upper_arm, right_forearm)

- [ ] **Test U.20**: Correct number of joints
  Expected: 5 joints (neck, left_shoulder, left_elbow, right_shoulder, right_elbow)

- [ ] **Test U.21**: All joint types are appropriate
  Expected: All joints are type "revolute"

- [ ] **Test U.22**: Inertial properties present for all links
  Expected: Mass and inertia values defined

- [ ] **Test U.23**: Visual geometries are reasonable
  Expected: Geometries (box, cylinder, sphere) with appropriate dimensions

- [ ] **Test U.24**: Collision geometries present
  Expected: All links have collision geometry

- [ ] **Test U.25**: Materials defined for visualization
  Expected: At least basic colors defined for visual elements

## Test Execution Order

**Recommended testing sequence**:

1. Pre-Testing Setup (all items)
2. hello_world_node.py (all tests)
3. simple_talker.py (all tests)
4. simple_listener.py (all tests)
5. simple_service.py (all tests)
6. Integration Testing (all tests)
7. Error Handling Testing (all tests)
8. Code Quality Verification (all tests)
9. Performance Testing (all tests)
10. Testing Environment Verification (all tests)
11. simple_humanoid.urdf (all tests)
12. check_urdf_example.sh (all tests)
13. URDF Visualization Testing (all tests)
14. URDF Structure Verification (all tests)

## Test Results Summary

**Total Tests**: 50+ test items

**Pass Criteria**:
- All Pre-Testing Setup items: ✅ PASS
- All functional tests: ✅ PASS
- All integration tests: ✅ PASS
- All PEP 8 compliance: ✅ PASS (0 errors)
- All documentation tests: ✅ PASS
- All humanoid context tests: ✅ PASS

**Overall Status**: ⬜ NOT TESTED | ✅ PASS | ❌ FAIL

**Notes**:
- Record any failures with specific error messages
- Document any workarounds or environmental issues
- Note any OS-specific problems (macOS, WSL2, etc.)

## Next Steps After Testing

1. **If All Tests Pass**: Proceed to Chapter 2 implementation
2. **If Tests Fail**:
   - Document failure in PHR
   - Fix code or update setup instructions
   - Re-test until all tests pass
3. **Record Test Results**: Update this checklist with actual test dates and results

---

**Testing Completed By**: ______________________
**Date**: ______________________
**ROS 2 Version**: ______________________
**Ubuntu Version**: ______________________
**Python Version**: ______________________
