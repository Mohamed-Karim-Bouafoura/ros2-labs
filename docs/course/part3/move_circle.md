---
title: "A move_circle.py Worked Example" 
---

A working `move_circle.py` node (from [Part 2 Exercise 5](../part2.md#ex5)) complete with a proper shutdown procedure. Use this as a starting point for your `param_circle.py` node for the Part 3 Parameters Exercise.

## The Code

```python title="move_circle.py"
--8<-- "https://raw.githubusercontent.com/tom-howard/com2009_exercises/refs/heads/jazzy/part2_navigation/scripts/move_circle.py"
```

## Adding Package Dependencies

Make sure you define this node's dependencies within your package's `package.xml` file.

Find this line:

```xml title="package.xml"
...
<exec_depend>geometry_msgs</exec_depend>
...
```
