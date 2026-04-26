from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')


    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        
        Node(
            package='drone_autonomy',
            executable='px4_odom_bridge',
            name='px4_odom_bridge',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_camera_link',
            arguments=['0.14', '0', '0.22', '0', '0', '0', 'base_link', 'camera_link'],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_lidar_link',
            arguments=['0.12', '0', '0.26', '0', '0', '0', 'base_link', 'link'],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
            }],
        ),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen', # log for log file output
            parameters=[{
                'use_sim_time': use_sim_time,

                # Frame Setup
                'frame_id': 'base_link',
                'map_frame_id': 'map',

                # Sensor Subscriptions
                'subscribe_depth': False,
                'subscribe_scan_cloud': True,
                'subscribe_scan': False,
                'approx_sync': True,        # Sync Lidar and cam
                'queue_size': 10,           # buffer

                # Memory
                'Mem/IncrementalMemory': 'true',    # Build map from scratch instead of finding where drone is in a pre generated map
                'Mem/InitWMWithAllNodes': 'false',  # Load a map from DB if true
                'Mem/STMSize': '30',                # How many recent nodes stay in short-term memory before moving to WM
                'database_path': '/tmp/rtabmap.db', # Explicit path — delete this file for a fresh start

                # Visual Features
                'Kp/MaxFeatures': '500',        # Maximum number of visual keypoints to extract per frame.
                'Kp/DetectorStrategy': '8',     # ORB (feature detector algo)
                'Vis/FeatureType': '8',         # ORB for visual matches
                'Vis/MinInliers': '8',          # Minimum good feature matches to accept a visual link

                # Registration
                # How RTAB-Map aligns new observations to the map
                # 0 = visual only, 1 = ICP only, 2 = visual + ICP
                # With depth cam + LiDAR you have both, so use 2
                'Reg/Strategy': '2',
                'Reg/Force3DoF': 'false',                   # false because we want full 3D with the depth camera
                                                            # set true if you only want 2D
                # ICP (scan matching for LiDAR)
                "Icp/MaxCorrespondenceDistance": '0.15',    # Max distance between mathced scan points (meters)
                'Icp/VoxelSize': '0.05',                    # Downsample scans to 5cm before matching, speeds it up
                'Icp/PointToPlane': 'true',                 # True for 3D lidar point cloud

                # Loop Closure
                'RGBD/ProximityBySpace': 'true',            # Check for loop closure when near old nodes
                'RGBD/ProximityMaxGraphDepth': '0',         # 0 = check all nodes, not just recent neighbors
                'RGBD/ProximityPathMaxNeighbors': '10',
                'RGBD/OptimizeFromGraphEnd': 'false',       # Optimize from first node, keep origin stable

                # Keyfram Thresholds
                'RGBD/LinearUpdate': '0.1',         # Add new node after 10cm Movement
                'RGBD/AngularUpdate': '0.1',        # Add new node after ~6 degree rotation

                # Occupancy Grid (3D)
                'Grid/Sensor': '0',                 # scan_cloud is stored as scan in SensorData; 0=scan for grid
                'Grid/FromDepth': 'false',
                'Grid/RangeMax': '5.0',             # Max depth range to use, depth cameras get noitsy past 5m
                'Grid/RangeMin': '0.3',             # Ignore depth closer than 30cm
                'Grid/CellSize': '0.05',            # 5cm resolution
                'Grid/3D': 'true',                  # Enable 3D occupancy grid (octomap)
                'Grid/GroundIsObstacle': 'false',   # Don't mark the floor as obstacle
                'Grid/MaxGroundHeight': '0.1',      # Anything below 10cm is ground
                'Grid/MaxObstacleHeight': '3.0',    # Ignore points above 3m (ceiling)
                'Grid/MinClusterSize': '3',         # Need at least 3 cells to count as an obstacle, filters noise

                # --- Optimizer ---
                'subscribe_imu': True,
                'topic_queue_size': 30,
                'sync_queue_size': 30,
                'Optimizer/Strategy': '1',          # g2o - fixes drift when loop closures are detected
                'Optimizer/Iterations': '20',       # More iterations = more accurate but slower. 20 is standard
                'Optimizer/GravitySigma': '0.3',    # How much to trust IMU gravity for pitch/roll correction
            }],

            # --- Topic Remappings ---
            # Left side = what RTAB-Map expects
            # Right side = what YOUR drone actually publishes
            # CHANGE the right side to match your real topics
            # Find yours with: ros2 topic list | grep -E "camera|scan|odom"
            remappings=[
                ('rgb/image',       '/world/default/model/x500_lidar_2d_0/link/camera_link/sensor/IMX214/image'),
                ('rgb/camera_info', '/world/default/model/x500_lidar_2d_0/link/camera_link/sensor/IMX214/camera_info'),
                ('scan_cloud',       '/depth_camera/points'),
                ('scan',            '/world/default/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan'),
                ('odom',            '/odom'),
                ('imu',             '/world/default/model/x500_lidar_2d_0/link/camera_link/sensor/camera_imu/imu'),
            ],
        ),
    ])
