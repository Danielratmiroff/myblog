[category]: <> (guides)
[date]: <> (2022/06/12)
[title]: <> (Load testing a server)
[color]: <> (purple)

**What is load testing?** ⁉️

Quoting wikipedia:

> Load testing generally refers to **the practice of modeling the expected usage of a software program by simulating multiple users accessing the program concurrently**. As such, this testing > is most relevant for multi-user systems; often one built using a client/server model, such as web servers.

## Let's get started! 🏁

**Installing requirements**
We are gonna load test our server using [locust](https://locust.io/), a simple and straight forward python library.
&nbsp;

Install locust by running:
``` bash
pip3 install locust
``` 
*If you don't have python or pip3 installed, please checkout the following links:*

> How to install python: (installation guide)[https://www.python.org/downloads/]

> How to install pip3: (installation guide)[https://pip.pypa.io/en/stable/installation/]

&nbsp;

Test the installation:
``` bash
locust -V
``` 

## Load testing
Create a python file `locustfile.py` and add the following code in it:


``` python
from locust import HttpUser, task

class  HelloWorldUser(HttpUser):
@task
def  hello_world(self):
    self.client.get("/") #URL that we will request
```

In the same folder, run:

``` bash
locust
```

You should see something similar to: 

![Terminal](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/loadtest/terminal-start.jpg)\
&nbsp;

Now, you can access **[http://localhost:8089/](http://localhost:8089/)** */ in your web-browser and you will see the locust UI

![Localhost UI](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/loadtest/locust.jpg)\
&nbsp;

> Configure according your preferred settings and off you go! 🏎️

&nbsp;

### Testing
![Testing Preview](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/loadtest/testing.jpg)\
&nbsp;

One you stop the ongoing test, you can analise your results using the different views that locust offers:

*e.g. Charts*

![Charts](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/loadtest/charts.jpg)\
&nbsp;

or you can simply use the terminal view 

![Terminal view](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/loadtest/result-terminal.jpg)\
&nbsp;

> Welldone! You have load tested a server using locust, congrats! 🎉

&nbsp;

---

## One step further, a more realistic test

Make a more realistic and suitable test by modifying the `locustfile` to your needs
&nbsp;

``` python
import time
from json import JSONDecodeError
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

# Waiting time after between each task ran by users
wait_time = between(1, 5) 

@task
def hello_world(self):
    self.client.get("/hello")
    self.client.get("/world")
    
# "3" refers to the task's weight (it's 3 times more likely to be ran)
@task(3) 
def view_items(self):
    for item_id in range(10):
        # group requests with different parameters together
        self.client.get(f"/item?id={item_id}", name="/item") 
        time.sleep(1)

# call an API and validate its response
with self.client.post("/", json={"foo": 42, "bar": 69}, catch_response=True) as response:
try:
    if response.json()["greeting"] != "hello":
        response.failure("Did not get expected value in greeting")
except JSONDecodeError:
    response.failure("Response could not be decoded as JSON")
except KeyError:
    response.failure("Response did not contain expected key 'greeting'")
```

&nbsp;

With locust you can test your server fairly quickly with its simple setup 

Its configuration is also well docummented, take a look at their official site: 
[Locust documentation](https://docs.locust.io/en/stable/writing-a-locustfile.html)
&nbsp;

> Happy load testing! 🛩️