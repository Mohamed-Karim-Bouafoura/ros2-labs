---  
title: "An Odometry Subscriber Node"
---

## The Initial Code

Having copied the `subscriber.py` file from your `part1_pubsub` package, you'll start out with [the code discussed here](../part1/subscriber.md).

Let's look at what we need to change now.

## From Simple Subscriber to Odom Subscriber

### Imports

We will generally rely on `rclpy` and the `Node` class from the `rclpy.node` library for most nodes that we will create, so our first two imports will remain the same. 

We won't be working with `String` type messages any more however, so we need to replace this line in order to import the correct message type. As we know from [earlier in Part 2](../part2.md#odometry-explained), the `/odom` topic uses messages of the type `nav_msgs/msg/Odometry`:

``` { .bash .no-copy }
$ ros2 topic info /odom
Type: nav_msgs/msg/Odometry
...
```

This tells us everything we need to know to construct the Python import statement correctly:

```py
from nav_msgs.msg import Odometry
```

You'll also need to import a mathematical tool from the `math` module:

```py
from math import atan2
```

(for reasons that will become clearer shortly.)

### Change the Class Name

Previously our class was called `#!python SimpleSubscriber()`, change this to something more appropriate now, e.g.: `#!python OdomSubscriber()`:

```py
class OdomSubscriber(Node):
```

### Initialising the Class

The structure of this remains largely the same, we just need to modify a few things: 

1. Change the name that is used to register the node on the ROS Network:

    ```python
    super().__init__("odom_subscriber")
    ```

1. Change the subscription parameters:

    ```python
    self.my_subscriber = self.create_subscription(
        msg_type=Odometry, # (1)!
        topic="/odom", # (2)!
        callback=self.msg_callback, 
        qos_profile=10,
    )
    ```

    1. `/odom` uses the Odometry message type (as imported above)
    2. The topic name is `/odom`. You can also omit the forward slash when defining this, so `#!py topic="odom"` would also work. 

1. The final thing we'll do inside our class' `__init__` method (after we've set up the subscriber) is initialise a counter:

    ```py
    self.counter = 0 
    ```

    The reason for this will be explained shortly...

### Calculating Euler Angles from Quaternions 

After the `#!py __init__` class method, define a new method inside the `#!py OdomSubscriber()` class, called `quaternion_to_euler`:

```py
def quaternion_to_euler(self, orientation):
    x = orientation.x
    y = orientation.y
    z = orientation.z
    w = orientation.w

    yaw = # TODO: calculate yaw...

    return yaw # (in radians)
```

This function will receive the orientation data from the `/odom` topic (in quaternions) and needs to output the `yaw` angle in radians. Your job now is to establish the actual conversion process. You can see how this is done by looking at the `tb3_tools.py` module within your `part2_navigation` package[^tb3-tools][^auto-addison]:

[^tb3-tools]: `tb3_tools.py` comes from the ROS 2 Package template, so you get this "for free" with every package that you create on this course!
[^auto-addison]: The Quaternion to Euler conversion process is taken from [this Automatic Addison blog post](https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/){target="_blank"}.


``` { .txt .no-copy }
.
├── CMakeLists.txt
├── package.xml
├── part2_navigation_modules
│   ├── __init__.py
│   └── tb3_tools.py <-- See here!
└── scripts
    ├── basic_velocity_control.py
    ├── odom_subscriber.py
    └── stop_me.py

```

Implement the calculation so that your `quaternion_to_euler()` method actually outputs a correct yaw angle (in radians) for the robot.

 

### Modifying the Message Callback

Head to the existing `msg_callback` class method now and change this as follows:

```py
def msg_callback(self, topic_message: Odometry): # (1)!

    pose = topic_message.pose.pose # (2)!
    
    # (3)!
    pos_x = pose.position.x
    pos_y = pose.position.y
    pos_z = pose.position.z
    
    yaw = self.quaternion_to_euler(pose.orientation) # (4)!

    if self.counter > 10: # (5)!
        self.counter = 0
        self.get_logger().info(
            f"x = {pos_x:.3f} (m), y = ? (m), yaw = ? (radians)"
        ) # (6)!
    else:
        self.counter += 1

```

1. This is a *type annotation*. The topic that we are subscribing to has changed (previously `/my_topic`, now `/odom`), and the new topic uses a different datatype (a.k.a. "ROS Interface"). We therefore update the type annotation to match the new type of data that will be entering this callback method (via the `topic_mesage` variable).
2. We're only really interested in the Pose part of the odometry data, so we assign this to a variable.

3. As we know by now, Pose contains information about both the "position" and "orientation" of the robot, we extract the position values first and assign them to the variables `pos_x`, `pos_y` and `pos_z`.
    
    Position data is provided in meters, so we don't need to do any conversion on this and can use the data directly.

4. Orientation data is in quaternions, so we need to convert this to a Euler angle representation. We're calling a class method called `self.quaternion_to_euler()` to handle this conversion, which you should have established in the previous step.

5. Here we print out the values that we're interested in to the terminal.

    This callback function will execute every time a new message is published to the `odom` topic, which occurs at a rate of around 20 times per second (20 Hz).
        
    ??? tip
        We can use he `ros2 topic hz` function to tell us this:

        ``` { .txt .no-copy }
        $ ros2 topic hz /odom
        average rate: 18.358
        min: 0.037s max: 0.088s std dev: 0.01444s window: 20
        ``` 
    
    That's a lot of messages to be printed to the terminal every second! We therefore use an `if` statement and a `counter` to ensure that our `print` statement only executes for 1 in every 10 topic messages instead.

6. **Task**: Continue formatting the `print` message to display the three odometry values that are relevant to our robot!  

### Updating "Main"

The only thing left to do now is update any relevant parts of the `main` function to ensure that you are instantiating, spinning and shutting down your node correctly.

## Package Dependencies

Once again, we're importing a couple of Python libraries into our node here, which means that our package has two *dependencies*: `rclpy` and `nav_msgs`:

```py
import rclpy 
from rclpy.node import Node

from nav_msgs.msg import Odometry
```

We should therefore add these dependencies to our `package.xml` file (`part2_navigation/package.xml`). Open it up and find the following line:

```xml
<exec_depend>rclpy</exec_depend>
```

The package template already includes a dependency for `rclpy`, since this is pretty fundamental to our work here, but we do need to add `nav_msgs` as well, so add the following additional line underneath:

```xml
<exec_depend>nav_msgs</exec_depend>
```

Save the file and close it.
