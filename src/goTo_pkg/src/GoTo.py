#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


#Class which will contains all the aspects as publisher, subscriber, position
class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('Turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10)
                                                 #Topic+type of mess + queue for backup
        
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber("/turtle1/pose",Pose, self.update_pose)
        self.pose = Pose()   #current position
        self.rate = rospy.Rate(10)
        #initiation of the goal
        self.x_desired = 0
        self.y_desired = 0
        self.distance_tolerance = 0.01

    #The update_pose method is a callback function which will be used by the subscriber: 
    #it will get the turtle current pose and save it in the self.pose attribute: 
    def update_pose(self, data):
        self.pose.x = data.x 
        self.pose.y = data.y 
        self.pose.theta=data.theta
        print(self.pose)

    def euclidean_distance(self):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((self.x_desired - self.pose.x), 2) +
                pow((self.y_desired - self.pose.y), 2))
    
    def linear_vel(self):
        rospy.set_param("Beta",1.5)
        beta=rospy.get_param("Beta")
        return beta * self.euclidean_distance()

    def steering_angle(self):
        return atan2(self.y_desired - self.pose.y, self.x_desired - self.pose.x)

    def angular_vel(self):
        #as the odom only publish quantrion angle not euler so we use ready made function to euler an
        rospy.set_param("phy",6)
        phy=rospy.get_param("phy")
        return phy * (self.steering_angle() - self.pose.theta )

    def move2goal(self):
        rospy.set_param("X_goal",3)
        self.x_desired=rospy.get_param("X_goal")
        self.y_desired=rospy.get_param("y_goal")
        

        vel_msg = Twist()
        while self.euclidean_distance() >= self.distance_tolerance:
            vel_msg.linear.x = self.linear_vel()
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = self.angular_vel()
            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            # Publish at the desired rate.
            self.rate.sleep()
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.0
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass