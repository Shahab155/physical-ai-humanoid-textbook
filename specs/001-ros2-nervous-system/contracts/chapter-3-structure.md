# Chapter 3 Structure Contract: Humanoid Robot URDF

**Chapter**: 3
**Title**: "Humanoid Robot URDF: Modeling the Physical Body"
**User Story**: US3 (Construct Humanoid Robot URDF)
**Priority**: P3
**Prerequisites**: Chapter 1 and 2 completed
**Status**: Draft

## Chapter Specification

### Learning Objectives

By the end of this chapter, learners will be able to:

1. **Explain** the purpose and structure of URDF files
2. **Create** a URDF defining links and joints for a humanoid robot
3. **Validate** URDF files using the check_urdf tool
4. **Visualize** robot models in RViz or Gazebo
5. **Interpret** joint hierarchies and coordinate frames

### Content Structure

**Target Word Count**: 800-1000 words

#### Section 1: Introduction to Robot Modeling (100-150 words)
- What is URDF and why it's needed
- From abstract control to physical robots
- The connection to previous chapters (controlling what you define)
- Prerequisites: Understanding of coordinate frames

#### Section 2: URDF Fundamentals (200-250 words)
- XML-based robot description format
- Links: Physical components (body parts)
- Joints: Connections between links (articulations)
- Joint types: revolute, prismatic, fixed, continuous
- Coordinate frames and transformations
- Visual vs. collision vs. inertial properties

#### Section 3: Designing a Simple Humanoid (200-250 words)
- Hierarchical structure: torso → arms → hands
- Joint placement and degrees of freedom (DOF)
- Simplified humanoid for learning:
  - Torso (base link)
  - 2 arms (shoulder, elbow, wrist)
  - Head (optional)
- Why we start simple (learn fundamentals before complexity)

#### Section 4: Building the URDF (200-250 words)
- Step-by-step URDF construction
- Step 1: Base link (torso)
- Step 2: Adding shoulder joints
- Step 3: Adding arm links
- Step 4: Adding elbow and wrist joints
- Code example: `simple_humanoid.urdf` (complete file)
- Explanation of key URDF elements

#### Section 5: Validating and Visualizing (150-200 words)
- Using check_urdf tool
- Loading URDF in RViz for visualization
- Loading URDF in Gazebo for simulation
- Verifying joint limits and axes
- Common validation errors and fixes

#### Section 6: Extending the Model (100-150 words)
- Adding sensors (cameras, IMU)
- Adding grippers/hands
- Improving visual meshes
- From simple to realistic (future learning path)

#### Section 7: Common Pitfalls (100-150 words)
- Incorrect joint axes (wrong direction)
- Missing inertial properties (Gazebo warnings)
- Reference frame errors
- Unclosed XML tags

#### Section 8: Summary (100-150 words)
- Key takeaways
- URDF as the bridge between code and robot
- From defining to controlling (full circle)
- Next steps in robotics learning

### Code Examples

**Example 1: `simple_humanoid.urdf`** (80-120 lines)
```xml
<!-- Complete URDF for simple humanoid robot -->
<!-- Structure:
  - base_link (torso)
  - left_shoulder, left_elbow, left_wrist joints
  - right_shoulder, right_elbow, right_wrist joints
  - Simple box geometries for visualization
  - Joint limits for safety
-->
```

**Example 2: `check_urdf_example.sh`** (10-15 lines)
```bash
#!/bin/bash
# Script to validate URDF file
# Usage: ./check_urdf_example.sh path/to/robot.urdf
# Demonstrates: check_urdf tool, xacro (if needed)
```

### Troubleshooting Tips

1. **"Error: Link 'x' is not parent of any joint"**
   - Cause: Disconnected link in URDF tree
   - Solution: Ensure every link (except root) has parent joint

2. **"Joint axis points in wrong direction"**
   - Cause: Incorrect axis vector (e.g., "0 0 0" instead of "0 0 1")
   - Solution: Verify axis attribute matches joint rotation axis

3. **"Gazebo: robot falls through floor"**
   - Cause: Missing or incorrect inertial properties
   - Solution: Add mass and inertia matrix to each link

4. **"XML parsing error"**
   - Cause: Unclosed tag or malformed XML
   - Solution: Use XML validator, check matching tags

5. **"Robot doesn't appear in Gazebo"**
   - Cause: URDF not loaded or plugin missing
   - Solution: Check spawn_robot.py, verify robot description topic

### References

1. **URDF Tutorial**
   - URL: http://wiki.ros.org/urdf/Tutorials
   - Sections: Creating a URDF, Adding joints, Link elements

2. **URDF XML Specification**
   - URL: http://wiki.ros.org/urdf/XML
   - Sections: <link>, <joint>, <transmission>

3. **Gazebo URDF Reference**
   - URL: https://gazebosim.org/docs/fortrose/urdf
   - Sections: Gazebo-specific URDF tags, Plugins

### Validation Criteria

- [ ] Word count between 800-1000
- [ ] URDF example validates with check_urdf
- [ ] URDF loads successfully in Gazebo
- [ ] All 5 troubleshooting tips present
- [ ] Learning objectives are measurable
- [ ] All references accessible
- [ ] Humanoid robot structure (not other robot types)
- [ ] Joint hierarchy clearly explained

### Acceptance Tests

1. **URDF Creation Test**: Learner writes valid URDF with 3+ joints
2. **Validation Test**: URDF passes check_urdf with no errors
3. **Visualization Test**: URDF loads in RViz/Gazebo correctly
4. **Interpretation Test**: Learner explains joint hierarchy and parent-child relationships
5. **Independent Test**: Can create and validate URDF without reference (US3 requirement)

---

**Contract Version**: 1.0
**Last Updated**: 2026-03-03
**Status**: Ready for content creation
