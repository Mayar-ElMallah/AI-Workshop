#!/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


#Class which will contains all the aspects as publisher, subscriber, position
class TurtleBot:
    def _init_(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)
   
        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                     Twist, queue_size=10) 
                                                     #Topic+type of mess + queue for backup
   
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                   Pose, self.update_pose)
                                                   #Topic + type of message + callback function

        self.pose = Pose() #for initiation with the current data
        self.rate = rospy.Rate(10)
    
    
    #The update_pose method is a callback function which will be used by the subscriber: 
    #it will get the turtle current pose and save it in the self.pose attribute: 
    def update_pose(self, data):
        """Callleehback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)             #The nearest 4 numbers
        self.pose.y = round(self.pose.y, 4)
    
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                pow((goal_pose.y - self.pose.y), 2))
    
    def linear_vel(self, goal_pose):
        return rospy.get_param("Beta", 1.5) * self.euclidean_distance(goal_pose)
   
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
   
    def angular_vel(self, goal_pose):
        return rospy.get_param("phy",1.5) * (self.steering_angle(goal_pose) - self.pose.theta)
    
    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()
   
        # Get the input from the user.
        goal_pose.x = rospy.get_param("X_goal",5)
        goal_pose.y = rospy.get_param("y_goal",0)
   
        
        distance_tolerance = 0.01

   
        #we declare the vel_msg object, which will be published in '/turtle1/cmd_vel':
        vel_msg = Twist()  #the language of the message
   
        while self.euclidean_distance(goal_pose) >= distance_tolerance:
            

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)    #b3ml publish b3d ma zabat l variable 3shan tt7rk (execution step)

            # Publish at the desired rate.
            self.rate.sleep()
   
        # Stopping our robot after the movement is over as while loop is finished 
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
   
        # If we press control + C, the node will stop.
        rospy.spin()
 #Note: l  pose bya5od mn l values l bytlobha mno wl subscriber bysm3 w y update bl current posse w cmd_vel: execute those values
 # wl vel_mes  
if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
