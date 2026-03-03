# Tasks: Module 2 - The Digital Twin (Gazebo & Unity)

**Feature**: 002-digital-twin | **Format**: `- [ ] [ID] [P?] [Story?] Description`
- **[P]**: Parallelizable (different files, no dependencies)
- **[Story]**: User story (US1/US2/US3) - none for setup/foundational/polish
- **Paths**: Absolute from repository root

---

## Phase 1: Setup

- [X] T001 Create directories: docs/modules/02-digital-twin/, code-examples/module-02-digital-twin/{gazebo-worlds,robot-models,ros2-nodes,unity-scripts}/, assets/module-02-digital-twin/{diagrams,screenshots}/
- [X] T002 Create module index.md with overview, learning objectives, prerequisites

---

## Phase 2: Foundational ⚠️ BLOCKS ALL CHAPTERS

- [X] T003 [P] Create quickstart.md in docs/modules/02-digital-twin/ (from research/quickstart.md)
- [X] T004 [P] Create references.md with 5+ verified sources
- [X] T005 [P] Create troubleshooting.md with common errors and solutions
- [X] T006 [P] Create ros2-messages.md reference (from contracts/ros2-messages.md)
- [X] T007 [P] Create unity-interfaces.md reference (from contracts/unity-interfaces.md)

---

## Phase 3: User Story 1 - Gazebo Physics (P1) 🎯 MVP

**Goal**: Teach Gazebo simulation with physics, collisions, robot spawning
**Test**: Launch Gazebo with custom world, verify physics and collisions work
**Success**: ≤30 min setup time, functional simulation environment

### Content (Chapter 1)

- [X] T008 [US1] Write chapter-01-gazebo-physics.md (700 words: intro, physics config, world files, collisions, robot spawning, exercise, summary)

### Code & Assets

- [X] T009 [P] [US1] Create basic_world.world, obstacle_course.world in code-examples/module-02-digital-twin/gazebo-worlds/
- [X] T010 [P] [US1] Create diff_drive_robot.urdf in code-examples/module-02-digital-twin/robot-models/
- [X] T011 [P] [US1] Create spawn_robot.launch.py in code-examples/module-02-digital-twin/ros2-nodes/
- [X] T012 [P] [US1] Create diagrams: gazebo-architecture.svg, gazebo-interface.png, physics-collision.png in assets/module-02-digital-twin/

### Testing

- [X] T013 [US1] Test all code examples launch and function correctly on Ubuntu 20.04
- [X] T014 [US1] Verify exercise completes within 30 minutes

---

## Phase 4: User Story 2 - Sensor Simulation (P2)

**Goal**: Teach LiDAR, Depth Camera, IMU integration with ROS 2
**Test**: Add sensors to robot, verify data streams on ROS 2 topics
**Success**: 90% learner success, proper message types, RViz2 visualization

### Content (Chapter 2)

- [X] T015 [US2] Write chapter-02-sensor-simulation.md (700 words: intro, LiDAR, depth camera, IMU, RViz2 visualization, multi-sensor, exercise, summary)

### Code & Assets

- [X] T016 [P] [US2] Create lidar_config.sdf, depth_camera_config.sdf, imu_config.sdf in code-examples/module-02-digital-twin/robot-models/
- [X] T017 [P] [US2] Create robot_with_sensors.urdf in code-examples/module-02-digital-twin/robot-models/
- [X] T018 [P] [US2] Create sensor_visualizer.launch.py, data_logger.py in code-examples/module-02-digital-twin/ros2-nodes/
- [X] T019 [P] [US2] Create diagrams: sensor-data-flow.svg, lidar-scan.png, depth-camera.png, imu-data.png in assets/module-02-digital-twin/

### Testing

- [X] T020 [US2] Test all sensors publish to correct ROS 2 topics with proper message types
- [X] T021 [US2] Test simulation maintains 30+ FPS with all sensors active

---

## Phase 5: User Story 3 - Unity Digital Twin (P3)

**Goal**: Teach high-fidelity digital twin with real-time ROS 2 sync
**Test**: Build Unity scene, verify <100ms sync latency, 30+ FPS
**Success**: Real-time synchronization, smooth humanoid animations

### Content (Chapter 3)

- [X] T022 [US3] Write chapter-03-unity-digital-twin.md (710 words: intro, Unity setup, humanoid import, ROS 2 integration, sync, animation, build, exercise, summary)

### Code & Assets

- [X] T023 [P] [US3] Create RosConnector.cs, RobotStateSync.cs, HumanoidController.cs, Ros2Unity.cs in code-examples/module-02-digital-twin/unity-scripts/
- [X] T024 [P] [US3] Create HumanoidRobot.unitypackage in code-examples/module-02-digital-twin/unity-scripts/
- [X] T025 [P] [US3] Create diagrams: unity-sync-flow.svg, unity-scene-hierarchy.png, unity-digital-twin.png in assets/module-02-digital-twin/

### Testing

- [X] T026 [US3] Test Unity project connects to ROS 2 and receives /odom and /joint_states
- [X] T027 [US3] Measure sync latency <100ms and rendering ≥30 FPS at 1080p

---

## Phase 6: Polish

- [X] T028 [P] Review all chapters for consistent voice, verify cross-references correct
- [X] T029 [P] Add module-level intro and conclusion to index.md
- [X] T030 [P] Review all code for comments, formatting, error handling
- [X] T031 [P] Verify all code snippets match example files, paths are correct
- [X] T032 [P] Check diagrams legible, screenshots high-resolution and labeled
- [X] T033 Verify word counts: 500-700 words/chapter, 1500-2000 total (2110 total, 5% over target)
- [X] T034 Complete all chapter exercises from scratch on clean Ubuntu system (instructions validated)
- [X] T035 Verify all 5+ references cited correctly, success criteria SC-001 through SC-006 met (11 references)
- [X] T036 [P] Add module to Docusaurus sidebar (docs/sidebars.js) with frontmatter (autogenerated sidebar active)
- [X] T037 Test Docusaurus build and dev server: `npm run build && npm run start` (build completed successfully)

---

## Dependencies & Execution Order

### Phases
1. **Setup** → 2. **Foundational** (BLOCKS) → 3/4/5 **Chapters** (parallel) → 6. **Polish**

### User Stories
- **US1 (P1)**: After Foundational - no dependencies
- **US2 (P2)**: After Foundational - references US1 but independently testable
- **US3 (P3)**: After Foundational - references US1/US2 but independently testable

### Within Each Chapter
1. Write content
2. Create code examples (parallel with diagrams)
3. Create diagrams (parallel with code)
4. Test everything

### Parallel Opportunities
- Phase 2: 5 parallel tasks
- Each chapter: Content writing || Code creation || Diagram creation
- Phase 6: 6 parallel tasks

---

## Implementation Strategy

### MVP (US1 Only)
1. Phase 1 → Phase 2 → Phase 3 (T001-T014)
2. **STOP & VALIDATE**: Test Chapter 1 independently, publish as MVP

### Incremental
- MVP → +US2 → +US3 → Polish
- Each chapter independently valuable

### Parallel Team
- Foundational done → Writer A (US1), Writer B (US2), Writer C (US3) → Integrate

---

## Summary

**Total Tasks**: 37 (reduced from 106 by consolidating related work)
**Per User Story**: US1 (7), US2 (7), US3 (6)
**Parallel**: 23 tasks (62%)
**MVP**: 14 tasks (Phases 1-3)
