---
title: Describing the Humanoid
---

# Describing the Humanoid: An Introduction to URDF

To effectively control and simulate a robot, especially a complex one like a humanoid, the software system needs a precise understanding of its physical characteristics. The **Unified Robot Description Format (URDF)** serves this purpose in ROS-based systems, providing an XML format for describing the kinematics and dynamics of a robot.

## What is URDF?

URDF is an XML file format that represents a robot as a collection of rigid bodies (**links**) connected by various types of joints (**joints**). It allows you to specify:

*   **Links**: These define the physical and visual properties of each part of the robot. This includes:
    *   **Inertial properties**: Mass, center of mass, and inertia matrix, critical for dynamic simulation.
    *   **Visual properties**: The geometry (e.g., box, cylinder, mesh), color, and texture for rendering the robot in a simulator or visualization tool.
    *   **Collision properties**: A simplified geometry used for collision detection, which is often less detailed than the visual geometry to save computational resources.
*   **Joints**: These define how links are connected and their degrees of freedom. Common joint types include:
    *   **Revolute**: A rotating joint (e.g., a hinge, shoulder, elbow).
    *   **Continuous**: A revolute joint with no limits (e.g., a wheel).
    *   **Prismatic**: A sliding joint (e.g., a linear actuator).
    *   **Fixed**: A rigid connection with no relative motion.

## Importance for Humanoids

For humanoid robots, URDF is particularly crucial due to their complex articulated structure. A detailed and accurate URDF model enables:

*   **Kinematics and Dynamics**: Calculating the robot's pose (forward kinematics) or joint angles for a desired pose (inverse kinematics), and simulating its movement under various forces.
*   **Visualization**: Displaying the robot accurately in tools like RViz, allowing developers to monitor its state in real-time.
*   **Simulation**: Providing simulators (like Gazebo or NVIDIA Isaac Sim) with the necessary information to render the robot's geometry, apply physics, and detect collisions.
*   **Grasping and Manipulation**: Precisely defining end-effector positions and orientations for interaction with objects.

Creating a well-defined URDF is often the first step in bringing a new robot design into the ROS ecosystem, laying the groundwork for control, simulation, and advanced AI behaviors.