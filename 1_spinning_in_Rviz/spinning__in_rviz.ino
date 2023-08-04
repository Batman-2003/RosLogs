#include <ros.h>
#include <ros/time.h>
#include <tf/tf.h>
#include <Servo.h>
#include <tf/transform_broadcaster.h>
#include <std_msgs/UInt16.h>

float theta;
int degreesPrev = 0;

Servo servo;

ros::NodeHandle  nh;

geometry_msgs::TransformStamped t;
tf::TransformBroadcaster broadcaster;

char world_link[] = "/world_link";
char knob_link[] = "/knob_link";

void setup()
{
  nh.initNode();
  broadcaster.init(nh);
  servo.attach(9);
}

void loop()
{
  nh.spinOnce();
  int degrees = analogRead(A0);  
  float tmp = degrees * 3.14 / 180;
  theta = tmp;
  if (degreesPrev - degrees > 2 || degreesPrev - degrees < -2 )
  {
    servo.write(degrees);
  }
  degreesPrev = degrees;
  t.header.frame_id = world_link;
  t.child_frame_id = knob_link;

  t.transform.translation.x = 0.0;
  t.transform.translation.y = 0.0;
  t.transform.translation.z = 1.3;

  t.transform.rotation = tf::createQuaternionFromYaw(theta);
  t.header.stamp = nh.now();

  broadcaster.sendTransform(t);
  
  delay(1);
}
