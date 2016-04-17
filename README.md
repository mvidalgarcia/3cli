# 3cli
Cloud Computing Command Line Interface for AWS and CloudStack written in Python.

## Requirements
You should have your [boto](http://boto.cloudhackers.com/en/latest/) credentials set in advance. More info [here](http://boto.cloudhackers.com/en/latest/boto_config_tut.html#credentials).

##  Install

This project was tested under Python 2.7.10

Clone repository:

```bash
git clone https://github.com/mvidalgarcia/3cli.git
cd 3cli
```

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
