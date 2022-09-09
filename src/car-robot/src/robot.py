#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy

import tf
import turtlesim.msg
 
def handle_turtle_pose1(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                    rospy.Time.now(),
                    "turtle1",
                    "world")

def handle_turtle_pose2(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                    rospy.Time.now(),
                    "turtle2",
                    "world")

def handle_turtle_pose3(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                    rospy.Time.now(),
                    "turtle3",
                    "world")
   
rospy.Rate(10)
if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    #turtlename = rospy.get_param('~turtle')
    while(not rospy.is_shutdown()):
        rospy.Subscriber("turtle1",
                            turtlesim.msg.Pose,
                            handle_turtle_pose1)
        rospy.Subscriber("turtle2",
                            turtlesim.msg.Pose,
                            handle_turtle_pose2)
        rospy.Subscriber("turtle3",
                            turtlesim.msg.Pose,
                            handle_turtle_pose3)
    rospy.sleep()
    rospy.spin()
