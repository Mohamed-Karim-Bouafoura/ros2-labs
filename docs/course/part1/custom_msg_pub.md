---  
title: "The `Example` Message Publisher"
---

# The `Example` Message Publisher

## The Code

Copy **all** the code below into your `custom_msg_publisher.py` file and **review the annotations** to see what's different to the basic publisher from Exercise 5.

```py title="custom_msg_publisher.py"
--8<-- "code_templates/custom_msg_publisher.py"
```

1. We're now importing the `Example` message from our own `part1_pubsub` package.

2. We're also now declaring that `"my_topic"` will use the `Example` message data structure to send messages.

3. We need to deal with the topic messages differently now, to account for the more complex structure.

    We now populate our messages with two fields: `info` (a `string`) and `time` (an `int`). Identify what has changed here...
