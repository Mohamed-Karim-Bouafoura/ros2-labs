---  
title: Creating a Python Service Client
---

Copy **all** the code below into your `number_game_client.py` file and then **review the annotations** to understand how it all works.

```python title="number_game_client.py"
--8<-- "code_templates/number_game_client.py"
```

1. Creating a Service *Client* is done using the `create_client()` class method, providing the name of the service that we want to call (`srv_name`), and specifying the interface type used by it (`srv_type`). 

    `srv_type` and `srv_name` **must** match the definition in the server, in order to be able to communicate and send requests to it. 

2. We're declaring some parameters here (recall [Part 3](../part3.md#ex2)). We'll be using these differently this time however: *to create a command-line interface (CLI) for our node*. Essentially, we'll be setting these parameters dynamically when we call it with `ros2 run` (so that we can change the values each time we launch the client).

    We're defining two parameters for the node, to match the attributes of the service request:

    1.`"guess"`: An integer, with a default value of `0`. 
    2. `"cheat"`: A boolean, with a default value of `False`.

    (You'll see how this all works shortly, when we actually run the node.)

3. We use a `while` loop here to halt the execution of the code at this point and wait for the service to become available (if it isn't already). 

    We can't send a request to a service that isn't actually running!

4. In this class method we construct the service request and send it.
    
    (This method is called in the `main()` function below.)

5. Read the value of the `guess` parameter, which we'll set from the command-line when we call the node (with `ros2 run`).

    This has been split across three lines, otherwise it gets too long and runs off the screen!

6. Read the value of the `cheat` parameter, which we'll *also* set from the command-line (we'll look at this shortly).

    *Also* split across three lines for no reason other than readability!

7. Here we're printing the parameter values to the terminal as a log message, to confirm exactly what request will be sent to the server.

8. Here we actually construct the request, using a `part4_services/srv/MyNumberGame` interface class instance, as imported up at the top.

9. `#!py call_async(request)` then actually sends this request to the server.

10. We then call our client's `send_request()` class method, which in turn (as you know from above) will initiate the construction of the request and send it to the server. 

    The output of this function is the output of the `call_async(request)` call, which we assign to a variable called `future`.

11. We use the `rclpy.spin_until_future_complete()` method here, which (as the name suggests) will allow our node (`client`) to spin *only* until our service request (`future`) has completed. 

12. Once we've reached this point then the service has completed and returned its **Response**. 
    
    We obtain the response from our `future` object so that we can read its values...

13. To finish off, we construct a final log message containing the values returned by the Server (i.e. the **Response**). 
    
    We know what these attributes are called, because we defined them in the `MyNumberGame.srv` file, which we can recall at any point using `ros2 interface show`:

    ``` { .txt .no-copy }
    $ ros2 interface show part4_services/srv/MyNumberGame
    
    int32 guess
    bool cheat
    ---
    int32 num_guesses
    string hint
    bool correct
    ```
