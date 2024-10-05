import numpy as np
   from filterpy.kalman import KalmanFilter

   def sensor_fusion(robot_gps, robot_imu):
       kf = KalmanFilter(dim_x=4, dim_z=2)  # State: [x, y, vx, vy], Measurement: [x, y]
       
       # Initialize state transition matrix
       kf.F = np.array([[1, 0, 1, 0],
                        [0, 1, 0, 1],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
       
       # Measurement function
       kf.H = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0]])
       
       # Measurement noise covariance
       kf.R = np.eye(2) * 0.1**2
       
       # Process noise covariance
       kf.Q = np.eye(4) * 0.01**2
       
       # Initial state covariance
       kf.P *= 1000
       
       # Fuse GPS and IMU data
       kf.predict()
       kf.update(robot_gps)
       
       # Incorporate IMU data (simplified)
       kf.x[2:] += robot_imu
       
       return kf.x[:2]  # Return estimated position

   # Usage
   robot_gps = np.array([10.1, 20.2])  # GPS reading
   robot_imu = np.array([0.5, 0.3])    # IMU velocity reading
   fused_position = sensor_fusion(robot_gps, robot_imu)
   print(f"Fused robot position: {fused_position}")
