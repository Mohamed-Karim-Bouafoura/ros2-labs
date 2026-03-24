---  
title: "Lab 5: Actions"  
description: Learn about another key ROS communication method which is similar to a ROS Service, but with a few key benefits and alternative use-cases.
---

## Introduction

In this part of the course we'll learn about a third method of communication available in ROS: *Actions*.  Actions are essentially an advanced version of Services, and we'll look at exactly how these two differ and why you might choose to employ an action over a service for certain tasks. 

## Getting Started

**Step 1: Launch your ROS 2 Environment**

You should now have access to ROS 2 via a Linux terminal instance. We'll refer to this terminal instance as **TERMINAL 1**.


**Step 2: Launch VS Code** 

It's also worth launching VS Code now, so that it's ready to go for when you need it later on. 


**Step 3: Make Sure The Course Repo is Up-To-Date**

<a name="course-repo"></a>

In Lab 1 you should have [downloaded and installed The Course Repo](./part1.md#course-repo) into your ROS environment. If you haven't done this yet then go back and do it now. If you *have* already done it, then it's worth just making sure it's all up-to-date, so run the following command in **TERMINAL 1** now to do so:

```bash
cd ~/ros2_ws/src/ros/ && git pull
```

Then build with Colcon: 

```bash
cd ~/ros2_ws/ && colcon build --packages-up-to ros
```

And finally, re-source your environment:

```bash
source ~/.bashrc
```

!!! warning
    If you have any other terminal instances open, then you'll need run `source ~/.bashrc` in these too, in order for any changes made by the Colcon build process to propagate through to these as well.

## Calling an Action Server

Before we talk about what actions actually are, we're going to dive straight in and see one in *action* (excuse the pun). 

<!-- As you may remember from Part 3, you actually used a ROS Action to make your robot navigate autonomously in [Exercise 3](./part3.md#ex3), by calling an action server from the command-line. We will do a similar thing now, in a different context, and this time we'll also look at what's going on in a bit more detail. -->

#### Exercise 1: Launching an Action Server and calling it from the command-line {#ex1}

We'll play a little game here. We're going to launch our TurtleBot3 Waffle in a *mystery environment* now, and we're going to do this by launching Gazebo *headless* i.e. Gazebo will be running behind the scenes, but there'll be no Graphical User Interface (GUI) to show us what the environment actually looks like.  Then, we'll use an *action server* to make our robot scan the environment and take pictures for us, to reveal its surroundings!

1. To launch the TurtleBot3 Waffle in this *mystery environment*, use the following `ros2 launch` command in **TERMINAL 1**:

    ```bash
    ros2 launch simulations mystery_world.launch.py
    ```
    
    ... nothing will *appear* to happen (for now!)

1. Next, open up a new terminal (**TERMINAL 2**), and have a look at all the topics that are currently active on the ROS network (you should know exactly how to do this by now!)

    The output of this should confirm that ROS and our robot are indeed active...

    ??? question "How?"
        When the robot is active, the output of the `ros2 topic list` command should provide a long list of topics, a number of which we've been working with throughout this course so far, such as `cmd_vel`, `odom`, `scan`, and so on. If the Waffle simulation *isn't* active then we would be presented with a much smaller list, containing only the core ROS topics:

        ***
        **TERMINAL 2:**
        ``` { .bash .no-copy }
        $ ros2 topic list
        /parameter_events
        /rosout
        ```
        ***

1. Next (still in **TERMINAL 2**), run the following command to launch an *Action Server* on the network:

    ```bash
    ros2 run examples camera_sweep_action_server.py
    ```
    
1. Now, open up *another* new terminal instance (**TERMINAL 3**), but so that you can view this and **TERMINAL 2** side-by-side. Enter the following command to *list* all actions that are active on the ROS network:

    ```bash
    ros2 action list
    ```

    There should be an item here called `/camera_sweep`, use the `info` command to find out more about this:

    ```bash
    ros2 action info /camera_sweep
    ```

    This tells us the *name* of the action: `Action: /camera_sweep`, as well as the number of client and server nodes this action has. Currently, the action should have 0 *clients* and 1 *server*, and the node acting as the server here should be listed as `/camera_sweep_action_server_node` (the node that we just launched with the `ros2 run` command in **TERMINAL 2**).
    
    Finally, call the `ros2 action info` command again, but this time providing an additional argument:
    
    ```
    ros2 action info -t /camera_sweep
    ```

    ```
    Action: /camera_sweep
    Action clients: 0
    Action servers: 1
        /camera_sweep_action_server [interfaces/action/CameraSweep]
    ```

    The `-t` argument additionally shows the action *type* against the server node, indicating to us the type of *interface* used by the server.

1. Let's now find out more about the interface itself. As with any interface (message, service or action) we can use the `ros2 interface` command to do this. In **TERMINAL 3** enter the following:

    ```bash
    ros2 interface show interfaces/action/CameraSweep
    ```
    
    Which should present us with the following:

    ```txt
    --8<-- "https://raw.githubusercontent.com/tom-howard/tuos_ros/refs/heads/jazzy/tuos_interfaces/action/CameraSweep.action"
    ```
    
    There are three parts to an action interface, and we'll talk about these in a bit more detail later on, but for now, all we need to know is that in order to *call* an action, we need to send the action server a **Goal**.

    ??? info "Comparing with ROS Services"
        This is a bit like sending a **Request** to a ROS Service Server, like we did in the previous session.
    
1. We can issue a goal to an action server from the command-line using the `ros2 action` command again. Let's give this a go in **TERMINAL 3**.
    
    First, let's identify the right `ros2 action` sub-command:

    ```bash
    ros2 action --help
    ```

    ``` { .txt .no-copy}
    Commands:
      info       Print information about an action
      list       Output a list of action names
      send_goal  Send an action goal
    ```

    As above, there are three sub-commands to choose from, and we've already used the first two! Clearly, the `send_goal` command is the one we want now.

    Let's get some help on this one:

    ```bash
    ros2 action send_goal --help
    ```
    
    From this, we learn that there are three *positional arguments*, which must be supplied in the correct order:
    
    ``` { .bash .no-copy }
    ros2 action send_goal <action_name> <action_type> <goal>
    ```

    We know from our earlier interrogation with the `ros2 action list`, `info` and `ros2 interface show` commands how to provide the right data here:
    
    1. `action_name`: `/camera_sweep`
    1. `action_type`: `interfaces/action/CameraSweep`
    1. `goal`: a data packet (in YAML format) containing two parameters:
        1. `sweep_angle`: the angle (in degrees) that the robot will rotate on the spot (i.e. 'sweep')
        1. `image_count`: the number of images it will capture from its front-facing camera while 'sweeping'
    
1. Now, again in **TERMINAL 3**, have a go at using the `ros2 action send_goal` command, but keep an eye on **TERMINAL 2** as you do this:

    ``` { .bash .no-copy }
    ros2 action send_goal /camera_sweep interfaces/action/CameraSweep \
        "{sweep_angle: 0, image_count: 0}"
    ```

    Having called the action, you should then be presented with a message (in **TERMINAL 3**) that the `Goal was rejected.` In **TERMINAL 2** (where the action server is running), we should see some additional information about why this was the case. Read this, and then head back to **TERMINAL 3** and have another go at sending a goal to the action server, by supplying valid inputs this time!

    Once valid goal parameters have been supplied, the action server (in **TERMINAL 2**), will respond to inform you of what it's going to do. You'll then need to wait for it to do its job...

1. Once the action has completed (it could up to 20 seconds), a message should appear in **TERMINAL 3** to inform us of the outcome:
        
    ``` { .txt .no-copy }
    Result:
        image_paths: 
    - ~/ros_action_examples/img01.jpg
    - ~/ros_action_examples/img02.jpg
    - ~/ros_action_examples/img03.jpg
    - ...

    Goal finished with status: SUCCEEDED
    ```

    Additionally, we should see some further text in **TERMINAL 2** as well:

    ``` { .txt .no-copy }
    [INFO] [#####] [camera_sweep_action_server_node]: camera_sweep_action_server_node completed successfully:
      - Angular sweep = # degrees
      - Images captured = #
      - Time taken = # seconds
    ```

    1. The *result* of the action (presented to us in **TERMINAL 3**) is a series file paths, illustrating the images that have been captured, and where they have been saved on the filesystem. Navigate to this directory in **TERMINAL 3** (using `cd`) and have a look at the content using `ll` (a handy alias for the `ls` command):

        ```bash
        cd ~/ros_action_examples
        ```

        ```bash
        ll
        ```
            
        You should see the same number of image files in there as was requested with the `image_count` parameter.
    
    1. Launch `eog` in this directory and click through all the images to reveal your robot's *mystery environment*:

        ```bash
        eog .
        ```

1. Let's do this one more time. Close down the `eog` window, head back to **TERMINAL 3** and issue the `ros2 action send_goal` command again, but this time use the optional `-f` flag: <a name="send_goal_cli"></a>

    ```bash
    ros2 action send_goal -f /camera_sweep interfaces/action/CameraSweep \
        "{sweep_angle: 0, image_count: 0}" 
    ```

    !!! tip
        Don't forget to supply valid goal parameters again!

    *Now*, as well as being provided with a result once the action has completed, we're *also* provided with some regular updates while the action is in progress (aka *"feedback"*)! 

1. To finish off, close down the action server in **TERMINAL 2** and the headless Gazebo process in **TERMINAL 1** by entering ++ctrl+c++ in each terminal. 

## What is a ROS Action?

In the above exercise we launched an action server and then called it from the command-line using the `ros2 action send_goal` sub-command. In the same way as a ROS Service, the action also provided us with a **result** once the task had been completed.

Using the `-f` flag we were able to ask the server to provide us with *real-time feedback* on how it was getting on (in **TERMINAL 3**).  **Feedback** is one of the key features that differentiates a ROS Action from a ROS Service: An Action Server provides **feedback** at regular intervals whilst working towards its **goal**. Another feature of ROS Actions is that they can be *cancelled* part-way through (which we'll play around with shortly).

<figure markdown>
  ![](./part5/action_interface.png){width=400px}
</figure>

Ultimately, Actions use a combination of both Topic- *and* Service-based communication, to create a more advanced messaging protocol. Building on ROS Services, *Actions* are designed to be used for **longer running tasks**, due to the provision of *feedback* and the ability to *cancel* a process part-way through. You can read more about Actions in [the official ROS 2 documentation here](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html){target="_blank"} (which also includes a nice animation to explain how they work).

### The Format of Action Interfaces

Like Services, Action Interfaces have multiple parts to them, and we need to know what format these action messages take in order to be able to use them.

We ran `ros2 interface show` in the previous exercise, to interrogate the action interface used by the `/camera_sweep` action server:

```txt
ros2 interface show interfaces/action/CameraSweep
```

``` { .txt .no-copy }
--8<-- "https://raw.githubusercontent.com/tom-howard/ros/refs/heads/jazzy/interfaces/action/CameraSweep.action"
```

As we know from Exercise 1, in order to call this action server we need to send a **goal**, and (in this case) there are **two** goal parameters that must be provided:

1. `sweep_angle`: a 32-bit floating-point value
1. `image_count`: a 32-bit integer

!!! question "Questions"
    * What are the names of the **result** and **feedback** interface parameters? (There are three in total.)
    * What data types do these parameters use?

You'll learn how we use this information to develop Python Action Server & Client nodes in the following exercises.

## Creating Python Action Clients

In the previous exercise we *called* a pre-existing Action Server from the command-line, by sending a goal to it. Let's look at how we can do this from within a Python ROS node now.

### Exercise 2: Building a Python Action Client Node {#ex2}

1. In **TERMINAL 1** launch the *mystery world* simulation again, but this time with an additional argument:

    ```txt
    ros2 launch simulations mystery_world.launch.py with_gui:=true
    ```

    With the `with_gui` switch set to `true`, we should now be able to actually *see* the simulated world this time.

    <figure markdown>
      ![](../images/gz/coloured_pillars.png){width=600px}
    </figure>
    <center>*(Not really that exciting is it!?)*</center>

1. Then, in **TERMINAL 2**, launch the Camera Sweep Action Server again: 

    ```bash
    ros2 run examples camera_sweep_action_server.py
    ```

#### Part 1: A Minimal Action Client

1. Now, in **TERMINAL 3**, create a new package called `part5_actions` using [the approach that we've been using to create packages throughout this course](part1.md#ex4).

1. Navigate into the `scripts` folder of your package using the `cd` command:

    ```bash
    cd ~/ros2_ws/src/part5_actions/scripts/
    ```

1. In here, create a new Python file called `camera_sweep_action_client.py` (using the `touch` command) and make it executable ([using `chmod`](./part1.md#chmod)). 

1. Then, declare this as an executable in the package's `CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/camera_sweep_action_client.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. At an *absolute minimum*, the Action Client can be constructed as follows:

    <center>[:material-file-code-outline: The `camera_sweep_action_client.py` Node](./part5/minimal_action_client.md){ .md-button target="_blank"}</center>

1. Let's build the Node now, so that we can run it. Head back to **TERMINAL 3** and use Colcon to build the package: <a name="colcon"></a>

    ```bash
    cd ~/ros2_ws/ 
    ```

    ```bash
    colcon build --packages-select part5_actions --symlink-install
    ```

1. Re-source the `.bashrc`:

    ```bash
    source ~/.bashrc
    ```

1. Run your node with `ros2 run`:

    ```
    ros2 run part5_actions camera_sweep_action_client.py
    ```

    With the command above as it is, the server will reject the goal (check back in **TERMINAL 2** to find out why). How can you modify the above command (by adding some additional arguments), so that the `camera_sweep_action_client.py` node actually sends a valid goal?[^goal_params]

    [^goal_params]: You need to explicitly set the `goal_images` and `goal_angle` parameters at runtime, [much like we did here with the `number_game_client.py` service client](./part4.md#ex5).

1. Having modified the `ros2 run` command to successfully send a *valid* goal to the `camera_sweep` action server, the robot should start to turn, capturing images as it goes. 

    The Client that we've created here makes a call to the action server and then exits, it doesn't even wait for the server to finish its task! The only way that we'd know if the action was successful, is if we were to keep an eye on **TERMINAL 2**, to see the action *server* respond to the goal that was sent to it... The client itself provides no feedback during the action, nor the result at the end. Let's look to incorporate that now...

#### Part 2: Handling a Result

1. Go back to the `camera_sweep_action_client.py` file in VS Code.

1. In order to be able to handle the result that is sent from an action server, we first need to handle the response that the server sends to the goal itself.

    Within the `send_goal()` method of the `CameraSweepActionClient()` class, find the line that reads:

    ```py
    return self.actionclient.send_goal_async(goal)
    ```

    and change this to:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    self.send_goal_future.add_done_callback(self.goal_response_callback)
    ```

    This method is no longer returning the *future* that is sent from `send_goal_async()`, but is now handling this and adding a callback to it: `goal_response_callback`. This callback can now be used to inform the client of whether the server has *accepted* the goal or not.

1. We therefore need to define this callback now. Define it as a *new* class method of the `CameraSweepActionClient()` class (i.e. underneath the `send_goal()` class method that has already been defined)...

    ```py
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("The goal was rejected by the server.")
            return

        self.get_logger().info("The goal was accepted by the server.")

        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
    ```

    The *input* to this method will be the *future* that is created by the `send_goal_async()` call. We assign this to an attribute called `goal_handle` here, and can then use this for two purposes:

    1. To check if the goal that we sent was accepted by the server
    1. If it *was* accepted, then we can get the result (using `get_result_async()`) and we can attach *another* callback to this to actually process that result: `get_result_callback`.

1. Now we need to define this callback too. Define `get_result_callback` as another new method of the `CameraSweepActionClient()` class (i.e. underneath the `goal_response_callback()` class method that we have just defined)...

    ```py
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f"The action has completed.\n"
            f"Result (Image Paths):\n  "
            + "\n  ".join(result.image_paths)
        )
        rclpy.shutdown()
    ``` 

    The input to *this* class method is another future object which contains the actual result sent from the server. We assign this to `result` and use a `get_logger().info()` call to print this to the terminal when the action has finished.

    As we know from our work earlier, the `CameraSweep` Action interface contains one *Result* parameter called `image_paths`.

1. Finally, in the `main` method, change this:

    ```py
    future = action_client.send_goal()
    ```
    to just this:
    ```py
    action_client.send_goal()
    ```
    (because `#!py send_goal()` no longer returns a `future`)

1. And then also change: 
    ```py
    rclpy.spin_until_future_complete(action_client, future)
    ```

    to this:

    ```py
    rclpy.spin(action_client)
    ```

1. Save all your changes!

1. Run this node again now (with the `ros2 run` command) and observe the changes in action.

    Our client node now presents us with the *result* that is sent by the server on completion of the action, but wouldn't it be nice if we could see the real-time *feedback* as the action takes place? Let's add this in now...

#### Part 3: Handling Feedback

1. Go back to the `camera_sweep_action_client.py` file in VS Code.

1. In order to be able to handle the feedback that is sent from an action server, we need to add yet another callback! Go back to the `send_goal()` method and the line where we are actually sending the goal to the server:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    ```

    As it stands, all we're doing here is sending the goal, but we can also add a *feedback callback* to this too:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(
        goal=goal, 
        feedback_callback=self.feedback_callback
    )
    ```

    The `feedback_callback` will be executed every time a new feedback message is received from the server.

1. In order to define what we want to do with these feedback messages we need to add *yet another* new method to the `CameraSweepActionClient()` class. Underneath the `get_result_callback()` class method that we defined earlier, add this new one as well:

    ```py
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        fdbk_current_angle = feedback.current_angle
        fdbk_current_image = feedback.current_image
        self.get_logger().info(
            f"\nFEEDBACK:\n"
            f"  - Current angular position = {fdbk_current_angle:.1f} degrees.\n"
            f"  - Image(s) captured so far = {fdbk_current_image}."
        )
    ``` 

    As we know from our work earlier, the `CameraSweep` interface contains two *feedback* parameters: `current_angle` and `current_image`.

1. Save all your changes once again, run the node again with the `ros2 run` command and observe the changes in action.

    The node we've now built can send a *goal* to an action server, process the *feedback* returned from the server as the action is in progress, and present the *result* to us once everything is complete.
    
    As discussed earlier though, the *other* key feature of Actions is the ability to *cancel* them part-way through. So let's look at how to incorporate this now as well.

#### Part 4: Cancelling an Action

1. First, create a copy of your `camera_sweep_action_client.py` node and call it `cancel_camera_sweep.py`. Make sure **TERMINAL 3** is located in the `scripts` directory of your `part5_actions` package before running the following:

    ```bash
    cp camera_sweep_action_client.py cancel_camera_sweep.py
    ```
    
1. Don't forget to declare this as an *additional* executable in the package's `CMakeLists.txt`. You'll then also need to re-build the package with `colcon build` ([go back for a reminder](#colcon)).

1. Open the `cancel_camera_sweep.py` file in VS Code.

1. We want this client to be able to cancel the goal under two different circumstances:

    1. The client itself is shutdown by the user (via a ++ctrl+c++ in the terminal)
    1. A conditional event that happens as the action is underway.

    In order to address item 1 first, we need to draw upon some of the work we did in Part 2 in [the implementation of *safe shutdown procedures*](part2.md#ex5)...

1. As you hopefully recall, we first need to import `SignalHandlerOptions` into our node, so add this as an additional import at the start of the code:

    ```py
    from rclpy.signals import SignalHandlerOptions
    ```

    Then, in the `main()` node function, modify the `#!py rclpy.init()` call:

    ```py
    rclpy.init(
        args=args,
        signal_handler_options=SignalHandlerOptions.NO
    )
    ```

1. Inside the `#!py __init__()` method of our `CameraSweepActionClient()` class we now need to add some additional flags:

    ```py
    self.goal_succeeded = False
    self.goal_cancelled = False
    self.stop = False
    ```

    In the `get_result_callback()` class method, we can then ensure that the `self.goal_succeeded` flag is set to `True` when a result is received. In this class method, locate the `#!py rclpy.shutdown()` line and add the following *additional* line just above it:

    ```py
    self.goal_succeeded = True
    ```

1. Actions can be cancelled using a `cancel_goal_async()` method of the `goal_handle` that is obtained from the `goal_response_callback()`. As such, we need to make this accessible across our entire `CameraSweepActionClient()` class. Locate the `goal_response_callback()` class method, and add this line at the bottom as the last line of the `goal_response_callback()` method:

    ```py
    self.goal_handle = goal_handle
    ```

    This makes `goal_handle` accessible across the entire `CameraSweepActionClient()` class as `#!py self.goal_handle`. 

1. We can only attempt to cancel an Action when it's in progress, therefore the *feedback callback* is the best place to trigger this. Locate the `feedback_callback()` class method and place the following at the end of it:

    ```py
    if self.stop:
        future = self.goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancel_goal)
    ```

    Here, we call the `cancel_goal_async()` method from `self.goal_handle`, and add another new callback (`cancel_goal()`) to it (i.e. to encapsulate what we want to happen when the action is cancelled).

1. Now, let's define this as another new (and final!) class method:

    ```py
    def cancel_goal(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
            self.goal_cancelled = True
        else:
            self.get_logger().info('Goal failed to cancel')
    ```

    The input to this callback is another *future*, which we can use to determine if the goal has been cancelled (as shown above). If it *has*, then we set our `self.goal_cancelled` flag to `True`.

1. **Finally**, go back the `main()` function of the node. We're going to replace the `#!py rclpy.spin(action_client)` line now, with a `#!py rclpy.spin_once()`, wrapped inside a `#!py try` - `#!py except`, wrapped inside a `#!py while` loop!
    
    ```py
    while not action_client.goal_succeeded:
        try:
            rclpy.spin_once(action_client)
            if action_client.goal_cancelled:
                break
        except KeyboardInterrupt:
            print("Ctrl+C")
            action_client.stop = True
    ```

    The `#!py while` loop will execute until the action completes successfully, *or* until the goal is *cancelled*, *or* we shutdown the node with a ++ctrl+c++ interrupt.

    Look back through the node to see how all this will flow through your class.

1. We may wish to cancel a goal *conditionally* if - say - too much time has elapsed since the call was made, or the caller has been made aware of something else that has happened in the meantime (perhaps we're running out of storage space on the robot and can't save any more images!). 

    For the purposes of this exercise, we want to modify our node so that the action is always cancelled after a total of **5 images** have been captured. This can be done by making a fairly small modification to the `feedback_callback()`. **Have a go at implementing this now**. 

    * Have a go now at introducing a conditional call to the `cancel_goal()` method once a total of **5 images** have been captured.
    * You could use the `current_image` attribute from the `CameraSweepFeedback` message to trigger this.

### A Summary of ROS Actions

ROS Actions work a lot like ROS Services, but they have the following key differences:

1. They can be **cancelled**: If something is taking too long, or if something else has happened, then an Action Client can cancel an Action whenever it needs to.
1. They provide **feedback**: so that a client can monitor what is happening and act accordingly (i.e. cancel the action, if necessary).

This mechanism is therefore useful for operations that may take a long time to execute, and where intervention might be necessary.

## Creating Your Own Action Servers, Clients and Interfaces

!!! info "Important"
    Cancel *all* active processes that you may have running before moving on.

So far we have looked at how to call a pre-existing action server, but what about if we actually want to set up our own, and use our own custom Action Interfaces too? 

To start with, have a look at the Action Server that you've been working with in the previous exercises. You've been launching this with the following command:

``` { .bash .no-copy }
ros2 run examples camera_sweep_action_server.py
```

!!! question "Questions"
    * Which *package* does the action server node belong to?
    * Where (in that package directory) is this node likely to be located?

Once you've identified the name and the location of the source code, open it up in VS Code and have a look through it to see how it all works. Don't worry too much about all the content associated with obtaining and manipulating camera images in there, we'll learn more about this in [the next part of this course](./part6.md). Instead, focus on the general overall structure of the code and the way that the action server is implemented.

Some things to review:

1. The way the server is initialised and the numerous callbacks that are attached to it:
    
    ```py
    self.actionserver = ActionServer(
        node=self, 
        action_type=CameraSweep,
        action_name="camera_sweep",
        execute_callback=self.server_execution_callback, # (1)!
        callback_group=ReentrantCallbackGroup(), # (2)!
        goal_callback=self.goal_callback, # (3)!
        cancel_callback=self.cancel_callback # (4)!
    )
    ```

    1. This callback contains all the code that will be executed by the server once a valid goal is sent to it (i.e. the core functionality of the Action)
    2. This server node is set up as a *Multi-threaded Executor* (see the setup in `main()`), to control the execution of the various callbacks that we need. Here, we're assigning the Action Server to a *Reentrant Callback Group*, allowing all its callbacks to run in parallel, as well as other subscriber callbacks too. 
    3. This callback is used to check the goal parameters that have been sent to the server, to decide whether to accept or reject a request. 
    4. This callback contains everything that needs to happen in the event that the Action is *cancelled* part-way through.


1. Take a look at the various Action callbacks to see what's happening in each:

    1. How are **goal** parameters checked, and subsequently accepted or rejected?
    1. How are **cancellations** implemented, and how is this monitored in the main `server_execution_callback()`?
    1. How is **feedback** handled and published?
    1. How is the **result** handled and published too?

1. Finally, consider the shutdown operations.

### Implementing an "Exploration" strategy using the Action Framework {#explore}

An exploration strategy allows a robot to autonomously navigate an unknown environment while simultaneously avoiding crashing into things! One way to achieve this is to utilise two distinct motion states: moving forwards and turning on the spot, and repeatedly switching between them. *Brownian Motion* and *Levy Flight* are examples of this kind of approach. Randomising the time spent in either, or both, of these two states will result in a navigation strategy that allows a robot to slowly and randomly explore an environment. Forward motion could be performed until - say - a certain distance has been travelled, a set time has elapsed or something gets in the way. Likewise, the direction, speed and/or duration of turning could also be randomised to achieve this.

Over the next few exercises we'll construct our own Action Interface, Server and Client nodes with the aim of creating the *basis* for a basic exploration behaviour. Having completed these exercises you'll have something that - with further development - could be turned into an exploration type behaviour such as the above.

#### Exercise 3: Creating an Action Interface {#ex3}

In Exercise 2 we created the `part5_actions` package. Inside this package we will now define an Action *Interface* to be used by the subsequent Action Server and Client that we will create in the later exercises. 

1. Action interfaces must be defined within an `action` folder at the root of the package directory, so let's create this now in **TERMINAL 1**:

    1. First, navigate into your package:

        ```bash
        cd ~/ros2_ws/src/part5_actions
        ```
    
    1. Then use `mkdir` to make a new directory:

        ```bash
        mkdir action
        ```

1. In here we'll now define an Action Interface called `ExploreForward`:

    ```bash
    touch action/ExploreForward.action
    ```

1. Open this up in VS Code and define the data structure of the Interface as follows:

    ```txt title="ExploreForward.action"
    #goal
    float32 fwd_velocity               # The speed at which the robot should move forwards (m/s)
    float32 stopping_distance          # Minimum distance of an approaching obstacle before the robot stops (meters) 
    ---
    #result
    float32 total_distance_travelled   # Total distance travelled during the action (meters)
    float32 closest_obstacle           # LaserScan distance to the closest detected obstacle up ahead (meters)
    ---
    #feedback
    float32 current_distance_travelled # Distance travelled so far during the action (meters)
    ```

    This interface therefore has **two** goal parameters, **one** feedback parameter, and **two** result parameters:

    **Goal**:

    1. `fwd_velocity`: The speed (in m/s) at which the robot should move forwards when the action server is called. 
    1. `stopping_distance`: The distance (in meters) at which the robot should stop ahead of any objects or boundary walls that are in front of it (this data will come from `LaserScan` data from the robot's LiDAR sensor).
    
    **Feedback**:

    1. `current_distance_travelled`: The distance travelled (in meters) since the current action was initiated (based on `Odometry` data).

    **Result**:

    1. `total_distance_travelled`: The *total* distance travelled (in meters) over the course of the action (based on `Odometry` data).
    1. `closest_obstacle`: The distance to the closest obstacle up ahead of the robot when the action completes.

1. Now, declare this interface in the package's `CMakeLists.txt` file, so that the necessary Python code can be created:

    ```txt title="CMakeLists.txt"
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "action/ExploreForward.action" 
    )
    ```

1. Also modify the `package.xml` file (above the `#!xml <export>` line) to include the necessary `rosidl` dependencies:

    ```xml title="package.xml"
    <buildtool_depend>rosidl_default_generators</buildtool_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

1. Now run `colcon` to generate the necessary source code for this new interface: <a name="colcon-build-steps"></a>

    1. First, **always** make sure you're in the root of the Workspace:
        
        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Then run `colcon build`:

        ```bash
        colcon build --packages-select part5_actions --symlink-install 
        ```
    
    1. And finally re-source the `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. We can now verify that it worked. 

    1. Use `ros2 interface` to list all available interface types, but use the `-a` option to display only action-type interfaces:

        ```bash
        ros2 interface list -a
        ```

        Look for a message with the prefix "`part5_actions`".

    1. Next, *show* the data structure of the interface:

        ```bash
        ros2 interface show part5_actions/action/ExploreForward
        ```

        This should match the content of the `part5_actions/action/ExploreForward.action` file that we created above.

#### Exercise 4: Building the "ExploreForward" Action Server {#ex4}

1. In **TERMINAL 1** navigate to the `scripts` folder of your `part5_actions` package, then:
    
    1. Create a Python script called `explore_server.py`
    1. Make it executable
    1. Declare it as an executable in `CMakeLists.txt`

1. Open up the file in VS Code.

1. The job of the Server node is as follows:

    * The action server should make the robot move forwards until it detects an obstacle up ahead.
    * It should use the `ExploreForward.action` Interface that we created in the previous exercise. 
    * The Server will therefore need to be configured to accept two **goal** parameters:
        
        1. The speed (in m/s) at which the robot should move forwards when the action server is called. 
        1. The distance (in meters) at which the robot should stop ahead of any objects or boundary walls that are in front of it.
        
            To do this you'll need to subscribe to the `/scan` topic. Be aware that an object won't necessarily be directly in front of the robot, so you may need to monitor a range of `LaserScan` data points (within the `ranges` array) to make the collision avoidance effective (recall the [LaserScan callback example from Part 3](./part3/lidar_subscriber.md)).
    
    * Be sure to do some error checking on the goal parameters to ensure that a valid request is made. This is done by attaching a `goal_callback` to the Action Server. 

        * `fwd_velocity`: Should be a velocity that is moderate, and within [the robot's velocity limits](./part2.md#velocity_limits).
        * `stopping_distance`: Should be greater than the [minimum detectable limit of the LiDAR Sensor](./part3.md#range_max_min), large enough to safely avoid collisions. 

    * Whilst your server performs its task it should provide the following **feedback** to a Client:

        1. The distance travelled (in meters) since the current action was initiated.

            To do this you'll need to subscribe to the `/odom` topic. Remember the work that you did in Part 2 on this. 
            
            !!! tip "Tips" 
            
                * The robot's orientation shouldn't change over the course of a single action call, only its `linear.x` and `linear.y` positions should vary.
                * Bear in mind however that the robot won't necessarily be moving along the `X` or `Y` axis, so you will need to consider the total distance travelled in the `X-Y` plane.
                * We did this in the [Part 2 `move_square` exercise](./part2.md#ex6), so refer to this if you need a reminder.

    * Finally, on completion of the action, your server should be configured to provide the following **two** *result* parameters:
        1. The *total* distance travelled (in meters) over the course of the action.
        1. The distance to the obstacle that made the robot stop (if the action server has done its job properly, then this should be very similar to the `stopping_distance` that was provided by the Action Client in the **goal**).

1. There's some template code to help you with this:

    <center>[:material-file-code-outline: The `explore_server.py` Template](./part5/explore_server.md){ .md-button target="_blank"}</center>
    
    You might also want to take a look at the `camera_sweep_action_server.py` code from the earlier exercises to help you construct this: a lot of the techniques used here will be similar (excluding all the camera related stuff).  

**Testing**

When you want to test things out, why not use the *Nav World* environment from Part 3 (in **TERMINAL 1**):

```bash
ros2 launch simulations nav_world.launch.py
```

<figure markdown>
  ![](./part3/nav_world.png){width=600px}
</figure>

Don't forget that in order to launch the server you'll need to have built everything with `colcon` by following [the usual **three stage** process](#colcon-build-steps).

Do this in **TERMINAL 2**, and you'll then be able to run it:

```bash
ros2 run part5_actions explore_server.py
```

Also, don't forget that **you don't need to have developed a Python Client Node in order to test the server**. Use the `ros2 action send_goal` CLI tool to make calls to the server (like we did in [Exercise 1](#send_goal_cli)).

#### Exercise 5: Building a Basic "ExploreForward" Client {#ex5}

1. In **TERMINAL 3** navigate to the `scripts` folder of your `part5_actions` package, create a Python script called `explore_client.py`, make it executable, and add this to your `CMakeLists.txt`.

1. Run `colcon build` on it now, so you don't have to worry about it later (again, following the [**three stage** process as above](#colcon-build-steps))...

    Here it is again, for good measure:

    1. Step 1:
    
        ```bash
        cd ~/ros2_ws
        ```

    1. Step 2:

        ```bash
        colcon build --packages-select part5_actions --symlink-install
        ```

    1. Step 3:

        ```bash
        source ~/.bashrc
        ```
    
1. Open up the `explore_client.py` file in VS Code.

1. The job of the Action Client is as follows:

    * The client needs to issue a correctly formatted **goal** to the server.
    * The client should be programmed to monitor the **feedback** data from the Server.  If it detects (from the feedback) that the robot has travelled a distance *greater than 2 meters* without detecting an obstacle, then it should **cancel** the current action call.

1. Use the techniques that we used in the Client node from [Exercise 2](#ex2) as a guide to help you with this. 
    
    <!-- There's also [a code template here](./part5/search_client.md) to help you get started. <a name="ex4c_ret"></a> -->

1. Once you have everything in place, launch the action client with `ros2 run` as below:

    ```bash
    ros2 run part5_actions explore_client.py
    ```

    If all is good, then this client node should call the action server, which will (in turn) make the robot move forwards until it gets a certain distance away from an obstacle up ahead (`stopping_distance`), at which point the robot will stop, and your client node should then stop too. Once this happens, reorient your robot (using the `teleop_keyboard` node) and launch the client node again to make sure that it is robustly stopping in front of obstacles repeatedly, and when approaching them from a range of different angles. 

    !!! warning "Important"
        Make sure that your cancellation functionality works correctly too, ensuring that:
            
        1. The robot never moves any further than 2 meters during a given action call
        1. An action is aborted mid-way through if the client node is shut down with ++ctrl+c++

#### Exercise 6 (Advanced): Implementing an Exploration Strategy {#ex6}

Up to now, your Action Client node should have the capability to call the `ExploreForward.action` server to make the robot move forwards by 2 meters, or until it reaches an obstacle (whichever occurs first), but you *could* build on this now and turn it into a full exploration behaviour:

* Between action calls, your *client* node could make the robot turn on the spot to face a different direction and then issue a further action call to make the robot move forwards once again.
* The turning process could be done at random (*ideally*), or by a fixed amount every time.
* By programming your client node to repeat this process over and over again, the robot would (somewhat randomly) travel around its environment safely, stopping before it crashes into any obstacles and reorienting itself every time it stops moving forwards. 


## Submission on Google Classroom

To complete **Lab 5**, you must finish the final exploration challenge and upload your package.

### Final Challenge: The Exploration Node

Using the action server and client concepts you've learned, implement the exploration strategy discussed above. 

1. **The Goal**: Create a new node (e.g., `explore_action_client.py`) that uses the Action framework to make the robot autonomously navigate and explore the mystery environment without colliding with obstacles.
2. **The Logic**: 
    * Call the appropriate action server to move the robot.
    * Utilize feedback to monitor the robot's state.
    * Implement logic to cancel the current goal and issue a new one (e.g., turning) if an obstacle is detected or a certain amount of time has elapsed.

### Preparation for Upload

Ensure your `part5_actions` package is correctly compiled, free of build errors, and all Python scripts have executable permissions.

1.  **Clean your workspace**: 
    ```bash
    cd ~/ros2_ws/src/
    ```
2.  **Compress your package**: 
    ```bash
    zip -r part5_submission.zip part5_actions/
    ```

### Submission Checklist

Your `part5_submission.zip` must contain:

* **`scripts/`**: 
    1.  `camera_sweep_action_client.py` (From Exercise 2).
    2.  `cancel_camera_sweep.py` (The cancellation-capable version).
    3.  `explore_action_client.py` (**The Final Challenge**).
* **`package.xml`**: Must include all necessary dependencies (e.g., `rclpy`, `interfaces`, `action_msgs`).
* **`CMakeLists.txt`**: Correctly configured with all Python scripts listed under the `install(PROGRAMS ...)` block.

**Upload your `part5_submission.zip` to the "Lab 5: Actions" assignment on Google Classroom.**