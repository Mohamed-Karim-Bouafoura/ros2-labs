---
title: "Launch Files (Advanced)"
---

As we know from the work we've done in this course, ROS applications can be executed in two different ways:  

1. Using the `ros2 run` command:

    ``` { .bash .no-copy }
    ros2 run {Package name} {Node name}
    ```

1. Using the `ros2 launch` command:

    ``` { .bash .no-copy }
    ros2 launch {Package name} {Launch file}
    ```

The `ros2 launch` command, used in combination with *launch files*, offers a few advantages over `ros2 run`, for example:

1. **Multiple nodes** can be executed **simultaneously**.
1. From within one launch file, we can call *other* launch files.
1. We can pass in **additional arguments** to launch things conditionally, or to change the behaviour of our ROS applications *dynamically*.

Point 1 above is explored in [Part 3 of the ROS 2 Course](../part3.md) (Exercise 1). In this section we'll explore Points 2 & 3 further[^more].

[^more]: For more advanced launch file features, [have a look at this guide](https://github.com/MetroRobots/rosetta_launch){target="_blank"}.

!!! note
    Make sure you [check for updates to the course repo](./course-repo.md#updating) before moving on!

## Identifying Launch Arguments

We can use the `-s` option with `ros2 launch` to discover the additional arguments that can be supplied to any given launch file. Take the `waffle.launch.py` launch file from `tuos_simulations`, for example:

```bash
ros2 launch tuos_simulations waffle.launch.py -s
```

You should be presented with a range of arguments here, starting with:

``` { .txt .no-copy }
$ ros2 launch tuos_simulations waffle.launch.py -s
Arguments (pass arguments as '<name>:=<value>'):
urdf_file_name : turtlebot3_waffle.urdf

    'with_gui':
        Select whether to launch Gazebo with or without Gazebo Client (i.e. the GUI).
        (default: 'true')
```

Scroll to the *bottom* of the list, and you should see the following:

``` { .txt .no-copy }
    'x_pose':
        Starting X-position of the robot
        (default: '0.0')

    'y_pose':
        Starting Y-position of the robot
        (default: '0.0')

    'yaw':
        Starting orientation of the robot (radians)
        (default: '0.0')
```

Using these arguments, we can control the position and orientation of the Waffle when it is spawned into the simulated world. Try this:

```txt
ros2 launch tuos_simulations waffle.launch.py x_pose:=1 y_pose:=0.5
```

The robot should spawn into an empty world, but at coordinate position $x=1.0$, $y=0.5$, rather than $x=0$, $y=0$, as would normally be the case.

## Launching Launch Files from Launch Files!

As above, we learnt about how to create a basic launch file in [Part 3 of the ROS Course](../part3.md#ex1). Using what we learnt here, we can develop launch files to execute as many nodes as we want on a ROS network simultaneously. *Another* thing we can do with launch files however is launch *other* launch files! 

Think back to [Part 3 Exercise 2](../part3.md#ex2) now, where we explored **ROS 2 Parameters**. To explore this, we created a `param_circle.py` node (based on the `move_circle.py` node from Part 2) that would make the robot move in a circle at a radius dictated by the `radius` ROS parameter.

Ultimately, in order for this node to do *anything*, we must first have a robot simulation up and running, e.g.: 

``` { .bash .no-copy }
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

We could actually wrap the execution of the simulation *and* our `param_circle.py` node inside a single launch file, so that it can all be launched together using a single `ros2 launch` command...

!!! warning "Note"
    
    This exercise is here for illustration purposes.

    **DON'T** include launch descriptions for simulations in any work that you submit for course assignments! 

1. In a ROS 2 terminal, return to the `launch` directory of the `part3_beyond_basics` package. First, navigate into the package root:

    ```bash
    cd ~/ros2_ws/src/part3_beyond_basics
    ```

    ... and then into the `launch` directory from there:

    ```bash
    cd launch/
    ```

1. Make a new launch file in here, called `circle.launch.py`:

    ```bash
    touch circle.launch.py
    ```

1. Open this up in VS Code and enter the following:

    ```py title="circle.launch.py"
    from launch import LaunchDescription
    from launch_ros.actions import Node

    from launch.actions import IncludeLaunchDescription
    from launch.launch_description_sources import PythonLaunchDescriptionSource
    from launch.substitutions import PathJoinSubstitution
    from launch_ros.substitutions import FindPackageShare

    def generate_launch_description():
        return LaunchDescription([
            IncludeLaunchDescription( # (1)!
                PythonLaunchDescriptionSource( # (2)!
                    PathJoinSubstitution([ # (3)!
                        FindPackageShare("turtlebot3_gazebo"), # (4)!
                        "launch", 
                        "empty_world.launch.py" 
                    ])
                )
            )
        ])
    ``` 

    1. To include another launch file in a launch description, we use a `IncludeLaunchDescription()` class instance (imported from a module called `launch.actions`).
    2. We want to launch the "Empty World" simulation from the `turtlebot3_gazebo` package, which (as we know) can be done *from a terminal* with the following command:

        ``` { .bash .no-copy }
        ros2 launch turtlebot3_gazebo empty_world.launch.py
        ```

        Based on the above, we know that the launch file itself is a *Python* launch file, due to the `.py` file extension at the end.

        As such, the launch description that we want to include is a *Python* launch description, which must therefore be defined using a `PythonLaunchDescriptionSource()` instance (imported from a module called `launch.launch_description_sources`)
        
    3. The `PathJoinSubstitution()` class (from the `launch.substitutions` library) can be used to build file paths from a *list* of individual components (other file paths, folder names and launch file names).
        
        Here we're using this to construct a full file path to the launch file that we want to execute.

        ... but *how do we know what that is?* See below for more information...
    
    4. We need to know the *full path* to the launch file that we want to execute. We don't always know where this file is on our filesystem (launch files that are outside the ROS 2 workspace, that we haven't created ourselves for example).
    
        We can use another class called `FindPackageShare()` (from yet another library called `launch_ros.substitutions`). This provides us with the path to the *root* of this package directory.

        Installed ROS packages (including the ones that we create ourselves) are always located in - and executed from - a *"share"* directory, hence `FindPackageShare()`. There will be multiple *share* directories on our system:
            
        * `/opt/ros/jazzy/share/`
        * `~/ros2_ws/install/part3_beyond_basics/share/`
        
            ... for example.
            
    
    Currently, this launch file only contains the description of the `empty_world.launch.py` launch file from the `turtlebot3_gazebo` package. There's a few new things that have been introduced here to achieve this, so click on the :material-plus-circle: icons in the code above to find out what all these things are doing.

1. Now, add a `Node()` item to the launch description so that the `param_circle.py` node (from your `part3_beyond_basics` package) is launched *after* the "Empty World" simulation has been launched.

    Refer back to [Part 3 Exercise 1](../part3.md#ex1) for a reminder of how to do this.

1. [Run `colcon build` on your package](../part3.md#colcon-build) to *build* this new launch file.


1. Finally, when you're ready, execute your new `circle.launch.py` launch file:

    ```bash
    ros2 launch part3_beyond_basics circle.launch.py
    ```

If you've done this successfully, on launching the above command the Gazebo Empty World simulation should launch and, once it's loaded up, the robot should instantly start moving in a circle.

## Passing Launch Arguments

How do we pass an argument to a launch file (`tuos_simulations/waffle.launch.py`, for example) that is declared within *another* launch file? 

Taking the same approach as above, a basic launch description for the `tuos_simulations/waffle.launch.py` sim would look like this:

```py title="launch_args_example.launch.py"
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("tuos_simulations"),
                    "launch", 
                    "waffle.launch.py" 
                ])
            )
        )
    ])
```

To launch this *and* supply the `x_pose` and `y_pose` launch arguments to it as well, we need to add the following to the `PythonLaunchDescriptionSource()` definition:

```py
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        PathJoinSubstitution([
            FindPackageShare("tuos_simulations"), 
            "launch", 
            "waffle.launch.py"
        ])
    ),
    launch_arguments={ # (1)!
        'x_pose': '1.0',
        'y_pose': '0.5' # (2)!
    }.items()
)
```

1. Arguments are passed to the launch file via the `launch_arguments` option of `IncludeLaunchDescription()`.
2. Arguments are passed as a dictionary, which can contain multiple key value pairs separated by commas: `#!py dict = {key1:value1, key2:value2, ... }`. 
    
    In this case, *keys* are the names of the launch arguments to be passed to the `waffle.launch.py` launch file, and **values** are the actual values we want to assign to those arguments (and which can be changed as required).

## Command Line Arguments for Launch Files

To create arguments for our own launch files and to be able to pass these arguments into our own Nodes, we need to use **parameters**. Once again, we learnt about these in [Part 3 of the course](../part3.md#ex2) (in Exercise 2), where we created the `param_circle.py` node that has already been discussed above.

If you have a simulation still running, close this down now. For the remainder of this section, you should launch an empty world manually, from a separate terminal, whenever you need it (either the `tuos_simulations/waffle.launch.py` or `turtlebot3_gazebo/empty_world.launch.py` worlds would be appropriate).

### Declaring Command Line Arguments for Launch Files

Let's now create a very basic launch file called `cli_example.launch.py` now, to launch this node alone (once again, why not create this in your `part3_beyond_basics` package where you'll be building up quite a collection of launch files by now!):

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 

def generate_launch_description(): 
    return LaunchDescription([ 
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node' 
        )
    ])
```

As we know, this node uses a ROS 2 parameter called `radius` to control the size of the circle that the robot will follow. We can declare a value for this at run time from within this launch file and set its value via a command line argument passed to the launch file itself. 

To do this, we first use the `DeclareLaunchArgument` action, which must be included as an item in the `LaunchDescription`:

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument # (1)!

def generate_launch_description(): 
    return LaunchDescription([ 
        DeclareLaunchArgument(
            name='circle_radius', 
            description="Sets the desired radius of the circle (in meters).",
            default_value='1.0'
        ), # (2)!
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node' 
        )
    ])
```

1. We need to import `DeclareLaunchArgument` so that we can use it in the launch file.
2. Don't forget the comma to separate the two launch description items: `DeclareLaunchArgument()` and `Node()`! 

We're defining **three things** when declaring the launch argument:

1. `name`: The **name** of the argument.
2. `description`: A description of what this argument is used for.
3. `default_value`: A value that will be assigned if we don't provide one when executing the launch file.

### Passing Launch File Arguments to Python Nodes (via Parameters)

We defined a launch argument in the step above, but (currently) this argument isn't actually being passed to our `param_circle.py` node. To do this, we can add an argument to the `Node()` launch description item:

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration # (1)!

def generate_launch_description(): 
    return LaunchDescription([ 
        DeclareLaunchArgument(
            name='circle_radius', 
            description="Sets the desired radius of the circle (in meters).",
            default_value='1.0'
        ),
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node',
            parameters=[{'radius': LaunchConfiguration('circle_radius')}] 
        )
    ])
```

1. Another new import here!!

Remember that our `param_circle.py` node uses a parameter called `radius`, and we are passing this into *this launch file* using the value supplied by the *launch file* argument `circle_radius`. So, if we call this launch file *without* supplying the `circle_radius` argument, a default value of `1.0` will be set (instead of the default value of `0.5` set by the node itself). Test this out by running this launch file without passing a value for the `circle_radius` argument first:

```txt
ros2 launch part3_beyond_basics cli_example.launch.py
```

You should see regular messages printed to the terminal to indicate the radius that the node is attempting to achieve:

``` { .txt .no-copy}
...
[param_circle.py-1] [INFO] [###] [my_param_circle_node]: Moving with radius: 1.00 [m]
...
```

Now, do this again but this time specifying a value for `circle_radius`:

```txt
ros2 launch part3_beyond_basics cli_example.launch.py circle_radius:=0.3
```

This time, the regular status messages (and the movement of the robot) should have changed:

``` { .txt .no-copy}
...
[param_circle.py-1] [INFO] [###] [my_param_circle_node]: Moving with radius: 0.30 [m]
...
```

### Summary

In the above two sections we've seen how we can build a launch file that accepts a command line argument, and how we can pass the *value* of that command line argument into a ROS node.