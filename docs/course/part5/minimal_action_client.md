---  
title: A Minimal Action Client
---

## The Code

Review the code (including the annotations) and then take a copy of it.

```py title="camera_sweep_action_client.py"
--8<-- "code_templates/camera_sweep_action_client.py"
```

1. As you know by now, in order to develop ROS nodes using Python we need to import the `rclpy` client library, and the `Node` class to base our node upon. In addition, here we're also importing an `ActionClient` class too.  

2. We know that the `/camera_sweep` Action server uses the `CameraSweep` `action` interface from the `tuos_interfaces` package, so we import that here too (which we use to make a call to the server). 

3. Standard practice when we initialise ROS nodes: *we must give them a name*

4. Here, we instantiate an `ActionClient` class object. In doing this we define the `node` to add the action client too (in our case `self`, i.e. our `CameraSweepActionClient` class). We then also define the interface type used by the server (`CameraSweep`), and the name of the action that we want to call (`action_name="camera_sweep"`).

5. Here we're declaring two ROS parameters: `goal_images` and `goal_angle`. 

    We'll use these to set goals for the action server at runtime.

    By default, these values are set to `0`, so if we don't explicitly set values for these two parameters then they will remain at `0`!

    !!! question
        How do we set values for parameters at runtime (i.e. when we execute this node using `ros2 run`)?

        [Recall how we did this in Part 4](../part4.md#ex5). 

6. Here we define a class method to construct and deliver a goal to the server. 

7. As we know from earlier, a `CameraSweep.Goal()` contains two parameters that we can assign values to: `sweep_angle` and `image_count`.

    As above, the values assigned to these are derived from two ROS parameters: `goal_angle` and `goal_images`.

    !!! warning "Remember"
        By default, both parameters will have a value of `0` unless we explicitly assign a value to them (see above)!

        How do we assign values to these parameters at runtime? [Recall how we did this in Part 4](../part4.md#ex5).

8. The goal is sent to the server using the `send_goal_async()` method, which returns a *future*: i.e. something that will happen in the future, that we can wait on. This future is returned once the goal parameters have been accepted by the server, *not* when the action server has actually completed its job.
        
9. In our `main` method we initialise `rclpy` and our `CameraSweepActionClient` class (nothing new here), but then we call the `send_goal()` method of our class (as discussed above), which returns a *future*. We can then use the `rclpy.spin_until_future_complete()` method to spin up our node *only* until this future object has finished.

## Package Dependencies

The action client has *two key dependencies*, so we need to modify the `package.xml` file (below the `#!xml <exec_depend>rclpy</exec_depend>` line) to include these:

```xml title="package.xml"
<exec_depend>action_msgs</exec_depend>
<exec_depend>tuos_interfaces</exec_depend>
``` 
