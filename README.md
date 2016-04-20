# 3cli
Cloud Computing Command Line Interface for AWS and OpenStack written in Python.

This library uses [boto](http://boto.cloudhackers.com/en/latest/) to manage AWS and [Apache LibCloud](http://libcloud.apache.org/) to manage OpenStack.

Allows to perform the following operations:
##### AWS
* EC2  
  * List all running instances
  * Show information about an instance
  * Start an stopped instance
  * Stop a specific instance
  * Terminate all instances
  * Terminate a specific instance
  * List all volumes
  * Attach an existing volume to an instance
  * Detach a volume from an instance
  * Start a new instance (not previously addressed)
* S3
  * List all buckets
  * List all objects in a bucket
  * Upload an object
  * Download an object from bucket
  * Delete an object from bucket
* CloudWatch
  * Display AWS EC2 instance metrics
  * Set alarm (<40% CPU utilisation)
* RDS (Relational Database Service)
  * List DB instances
  * Show DB info
  * Create DB instance
  * Delete DB instance  
* Elastic Beanstalk
  * Create application
  * Delete application


##### OpenStack
* Compute  
  * List all running instances
* Storage
  * List all container
  * List all objects in a container
  * Upload an object to a container
  * Download an object from container
  * Delete an object from container

## Requirements

- You must have your boto credentials set in advance, more info [here](http://boto.cloudhackers.com/en/latest/boto_config_tut.html#credentials).  

- You must have a file called `trystack_api_key.cfg` in the project root folder with the following structure:
```
USER=<openstack_username>
API_KEY=<openstack_api_key>
```

##  Install

This project was tested under Python 2.7.10

Clone repository:

```bash
git clone https://github.com/mvidalgarcia/3cli.git
cd 3cli
```

I recommend using `virtualenv` to prevent installing dependencies in the machine.  
Create virtual environment:

```bash
virtualenv venv
```

Activate virtual environment:

```bash
. venv/bin/activate
```

Install dependencies:

```bash
pip install -r dependencies
```

Deactivate virtual environment:

```bash
deactivate
```

It is also possible not to use `virtualenv` and install the dependencies in the system with `pip`:

````
pip install boto
pip install apache-libcloud
```

## Run

Activate virtual environment:

```bash
. venv/bin/activate
```

Run server:
```bash
python run.py
```

Deactivate virtual environment:
```bash
deactivate
```

Note that virtual environment must be activated in order to run the app.
