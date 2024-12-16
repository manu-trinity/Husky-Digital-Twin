# Digital Twin of Husky Robot  

This repository provides a ROS2 Foxy simulation of the Husky robot integrated with multiple sensors, including Lidar, a camera, and a GPS sensor. The project focuses on creating a digital twin of the Husky robot for advanced robotics applications.

---




## Requirements  

- **Operating System**: Ubuntu 20.04  
- **ROS2 Version**: Foxy  
- **Gazebo Simulator**  
- **RViz** 


---

# Husky Robot Simulation with ROS2 Foxy  

This project integrates multiple sensors (Livox HAP Lidar, Stereolabs ZED2i Camera, and Emlid Reach RS2+ GPS) with a Husky robot simulation in ROS2 Foxy. The guide below covers building dependencies, running the simulation, and configuring the sensors.  

---
## Repository Structure  

The repository includes:  
1. **Livox-SDK2:** Precloned and ready for building.  
2. **Livox ROS2 Driver:** Precloned and set up.  
3. **Livox Lidar Simulation:** Precloned for integration.


## Building the Project 

### 1. Clone the Repository
Create a ROS2 workspace and clone the repository:
```bash
mkdir -p ~/husky_digital_twin/src
cd ~/husky_digital_twin/src
git clone https://code.ovgu.de/iks-ams/teaching/student-projects/husky_digital_twin.git
```

## Setting up of LIDAR
### Building the Livox SDK2
The Livox SDK2 is necessary for Lidar integration. Build it as follows:
```bash
cd ~/husky_digital_twin/src/Livox-SDK2/
mkdir build && cd build
cmake ..
make -j
sudo make install 
```  



### 2. Build the Workspace  
After building the Livox SDK, build the entire workspace:  
```bash  
cd ~/husky_digital_twin 
colcon build  
source install/setup.bash  
```  


## Running the Simulation  

To visualize the Husky robot with the integrated Livox Lidar in Gazebo and RViz:  

### Step 1: Launch Gazebo Simulation  
In the first terminal, launch the Gazebo simulation:  
```bash  
cd ~/husky_digital_twin  
source install/setup.bash  
ros2 launch husky_gazebo gazebo.launch.py  
```  

### Step 2: Launch RViz  
In the second terminal, wait for 30 seconds, then launch RViz:  
```bash  
cd ~/husky_digital_twin  
source install/setup.bash  
ros2 launch husky_viz view_model.launch.py  
```  

### Step 3:Move husky 
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---


## Adding a PointCloud2 Display in RViz for LIVOX HAP  

1. In RViz, click the **Add** button in the Displays panel. 

2. In the **By topic** tab, select the `/HAP_PointCloud2` topic. 

---


## Adding a PointCloud2 Display in RViz for Zed 2i (Depth )
1. In RViz, click the **Add** button in the Displays panel.  

2. In the **By topic** tab, select the `/zed2/points` topic.  

---

## Adding Images for ZED2i Cameras 

Left Camera:

  1. In RViz, click the **Add** button in the Displays panel. 

  2. In the **By topic** tab, under `/zed2_left_raw_camera` select `Image`.

Right Camera:

  1. In RViz, click the **Add** button in the Displays panel. 

  2. In the **By topic** tab, under `/zed2_right_raw_camera` select `Image`.



## Position of Husky using GPS Sensor
In a new terminal 

```bash  
cd ~/husky_digital_twin  
ros2 topic echo /reach_rs2/gps/data
``` 


## Sensor Integrations  

### 3D Models for Sensors  

The following sensors are integrated into the Husky robot simulation. STL files were sourced or converted for proper visualization:  

1. **Lidar Sensor: Livox HAP TX**  
   - **Source**: [Livox HAP Downloads](https://www.livoxtech.com/de/hap/downloads)  
   - **File Type**: STL (direct download)  

2. **Camera: Stereolabs ZED2i**  
   - **Source**: [Stereolabs 3D Models and Dimensions](https://support.stereolabs.com/hc/en-us/articles/360007494333-Can-I-get-3D-models-and-dimensions-of-my-device)  
   - **File Type**: STL (direct download)  

3. **GPS Sensor: Emlid Reach RS2+**  
   - **Source**: [Emlid Hardware Repository](https://github.com/emlid/hardware)  
   - **File Type**: STEP (STP) converted to STL using [Image to STL Online Converter](https://imagetostl.com/convert/file/stp/to/stl).
## Related Links  

### General Resources  
- [ROS2 Foxy Installation Guide](https://docs.ros.org/en/foxy/Installation.html)- Official instructions for installing ROS2 Foxy on Ubuntu 20.04. 
- [Gazebo Documentation: Getting Started](https://gazebosim.org/docs/latest/getstarted/) - Beginner's guide to setting up and using the Gazebo simulator.
- [The Construct Course: ROS2 Husky Simulation](https://www.theconstructsim.com/ros2-simulation-course-husky/) - Online course for learning Husky simulation in ROS2. 

### Husky  
- [Husky Official GitHub Repository](https://github.com/husky/husky/tree/foxy-devel)- Source code for Husky's ROS2 packages, including support for Foxy.  
- [Husky Simulator GitHub Repository](https://github.com/husky/husky_simulator) - A repository for Husky's Gazebo simulator and related packages.   
- [Husky Simulation Tutorial (ROS Wiki)](http://wiki.ros.org/husky_gazebo/Tutorials/Simulating%20Husky)- Step-by-step guide to simulate the Husky robot using Gazebo.  
- [Husky Documentation (OVGU GitLab)](https://code.ovgu.de/iks-ams/hardware/husky/husky-documentation) - Internal documentation repository for Husky robot at OVGU.  
  

### Livox HAP Lidar  
- [Livox ROS2 Plugin](https://github.com/LihanChen2004/livox_laser_simulation_ros2.git)  
- [Livox SDK2](https://github.com/Livox-SDK/Livox-SDK2.git)  
- [Livox Laser simulation](https://github.com/LihanChen2004/livox_laser_simulation_ros2.git)

### Stereolabs ZED2i Camera  
- [ZED ROS2 Wrapper](https://github.com/stereolabs/zed-ros2-wrapper/)  
- [ZED SDK](https://github.com/stereolabs/zed-sdk)  
- [Gazebo ROS Camera Integration](https://github.com/ros-simulation/gazebo_ros_pkgs/wiki/ROS-2-Migration:-Camera)
