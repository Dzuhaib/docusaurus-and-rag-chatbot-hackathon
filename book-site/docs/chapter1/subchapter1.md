---
title: Core Concepts of ROS 2
restricted: true
---

# Core Concepts of ROS 2: Nodes, Topics, and Services

The Robot Operating System (ROS) provides a flexible framework for writing robot software. ROS 2, a re-architected version, focuses on supporting multi-robot systems, real-time control, and a more robust communication infrastructure. Understanding its core concepts is fundamental to building any robot application.

## Nodes

A **Node** is an executable process that performs computation. In ROS 2, each node is designed to do a specific task, such as controlling a motor, reading sensor data, or performing a localization algorithm. Breaking down robot functionality into small, modular nodes makes the system more manageable, reusable, and fault-tolerant.

## Topics

**Topics** are the primary mechanism for asynchronous, many-to-many, anonymous communication in ROS 2. Nodes publish data to topics, and other nodes can subscribe to these topics to receive the data. This publish/subscribe model allows for loose coupling between components, meaning nodes don't need to know about each other's existence directly. Data transmitted over topics can be anything from sensor readings (e.g., LiDAR scans, camera images) to motor commands.

## Services

While topics are suitable for continuous data streams, **Services** are used for synchronous, request/reply interactions. A service call blocks the client node until the server node responds. This is ideal for actions that require a single, immediate result, such such as triggering a specific action (e.g., "capture image," "move arm to position") or querying a parameter. Each service defines a request and a response message type.

## Key Differences from ROS 1

ROS 2 introduces several improvements over its predecessor, including:
*   **DDS (Data Distribution Service)**: ROS 2 leverages DDS for its communication layer, providing better Quality of Service (QoS) settings for reliability, durability, and real-time performance.
*   **Security**: DDS-based communication allows for built-in security features like authentication and encryption.
*   **Multi-robot support**: Designed from the ground up to handle multiple robots in a coordinated fashion.

By mastering these core concepts, developers can effectively design and implement distributed robot control systems in ROS 2.