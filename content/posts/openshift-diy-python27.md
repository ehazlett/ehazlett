Date: 2012-05-15
Title: OpenShift: DIY Python2.7
Tags: [openshift, python]

## Preface

I have been using OpenShift for a few months now and have to say that I still love it.  I've sampled most of the other PaaS solutions and feel most comfortable with OpenShift.  One of the features I enjoy most in the service is the "do-it-yourself" application.  With this, you can run just about anything in a "minimal-hassle", scalable environment.

I created a quickstart a few weeks ago that had Django running on Python 2.7 in "DIY" mode.  This will use some of that, but be a more "step-by-step" approach for newcomers.  This example will use the [Flask](http://flask.pocoo.org/) micro-framework as well as the uWSGI application container for a true, production ready environment.

## Diving In

The first thing you will need to do is get an [OpenShift](http://openshift.redhat.com) account (it's free).

### Client Tools

Install the OpenShift client tools:

`gem install rhc`

** See [here](https://openshift.redhat.com/app/getting_started) if you have trouble getting the tools installed.

### Application Setup

Once you have the toolchain setup, we will create the application environment in OpenShift.  For this example, we will name our application "py27".

`rhc-create-app -a py27 -t diy-0.1`

You will see something similar to:


    Creating application: py27 in ehazlett
    Now your new domain name is being propagated worldwide (this might take a minute)...
    Confirming application 'py27' is available:  Success!

    py27 published:  http://py27-ehazlett.rhcloud.com/
    git url:  ssh://uuid1234567890@py27-ehazlett.rhcloud.com/~/git/py27.git/
    Disclaimer: This is an experimental cartridge that provides a way to try unsupported languages, frameworks, and middleware on Openshift.

You can view the bootstrapped application at `http://py27-[username].rhcloud.com`

### Python 2.7

Now that the application environment is created, we will build and install the latest Python 2.7.x release.  To do that, we will first need to get the application SSH credentials.

Run the following to show your application config (enter your account password when prompted):

`rhc app show -a py27`

You should see something similar to this:

    Application Info
    py27
        Framework: diy-0.1
         Creation: 2012-05-15T22:54:09-04:00
             UUID: 1qaz2wsx3edc4rfv
          Git URL: ssh://1qaz2wsx3edc4rfv@py27-ehazlett.rhcloud.com/~/git/py27.git/
       Public URL: http://py27-ehazlett.rhcloud.com/

     Embedded:
          None

Log into your OpenShift application using the SSH credentials from above (in the Git URL line):

`ssh 1qaz2wsx3edc4rfv@py27-[username].rhcloud.com`

We will build everything in the OpenShift application tmp directory.

Navigate into the "tmp" directory:

`cd $OPENSHIFT_TMP_DIR`

Download the latest Python 2.7.x release:

`wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2`

Extract:

`tar jxf Python-2.7.3.tar.bz2`

Configure (to put the custom Python into the OpenShift runtime dir):

`cd Python-2.7.3`

`./configure --prefix=$OPENSHIFT_RUNTIME_DIR`

Make and install:

`make install`

You can now check that Python was successfully installed:

`$OPENSHIFT_RUNTIME_DIR/bin/python -V`

You should get

    Python 2.7.3

### Supporting Tools

We now have Python installed, but we can't do much.  Part of the common Python toolchain is PIP for Python package management.

#### Setuptools

Change into the OpenShift "tmp" directory:

`cd $OPENSHIFT_TMP_DIR`

Download and install setuptools:

`wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz`

`tar zxf setuptools-0.6c11.tar.gz`

`cd cd setuptools-0.6c11`

Install:

`$OPENSHIFT_RUNTIME_DIR/bin/python setup.py install`

#### PIP

Change into the OpenShift "tmp" directory:

`cd $OPENSHIFT_TMP_DIR`

Download and install setuptools:

`wget http://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz`

`tar zxf pip-1.1.tar.gz`

`cd pip-1.1`

Install:

`$OPENSHIFT_RUNTIME_DIR/bin/python setup.py install`

#### uWSGI

We will be using the uWSGI application container to give a real-world working application setup.  This is high-performance and not a simple "runserver" example.

Change into the OpenShift "tmp" directory:

`cd $OPENSHIFT_TMP_DIR`

Install uWSGI:

`$OPENSHIFT_RUNTIME_DIR/bin/pip install uwsgi`

Check that uWSGI was installed properly:

`$OPENSHIFT_RUNTIME_DIR/bin/uwsgi --version`

You should see:

    1.2.3

### Application

Okay, so now we have all of the parts needed to run the app.  We now need to create the Flask application and configure OpenShift so that it knows how to start and stop it.

First we will create the Flask application. Logout of your OpenShift environment and navigate into the Git repository that was created for your app.

You should have a directory structure similar to the following:

    ├── README
    ├── diy
    │   └── index.html
    └── misc

Create a directory named "app" with a file named `application.py` and `__init__.py`:

    ├── README
    ├── app
    │   └── __init__.py
    │   └── application.py
    ├── diy
    │   └── index.html
    └── misc

Edit `application.py` with the following:

    from flask import Flask
    import platform
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello from Flask'

    @app.route('/info')
    def info():
        return platform.python_version()

Create a `requirements.txt` in the root application directory with the following:

    Flask==0.8

Directory structure should look like:

    ├── README
    ├── app
    │   └── __init__.py
    │   └── application.py
    ├── diy
    │   └── index.html
    ├── misc
    └── requirements.txt

### Hooks

We will now create the hooks that are needed for deployment as well as for starting and stopping the application.  In your application Git repository, there is a hidden directory called ".openshift" that contains stubs for the action hooks.  We will be editing these.

Edit `.openshift/action_hooks/build` to have the following:

```
    #!/bin/bash
    $OPENSHIFT_RUNTIME_DIR/bin/pip install --use-mirrors -r $OPENSHIFT_REPO_DIR/requirements.txt
```

Edit `.openshift/action_hooks/start` to have the following:

```
    #!/bin/bash
    cd $OPENSHIFT_REPO_DIR
    $OPENSHIFT_RUNTIME_DIR/bin/uwsgi --http $OPENSHIFT_INTERNAL_IP:8080 --module application:app --pp $OPENSHIFT_REPO_DIR/app -d $OPENSHIFT_LOG_DIR/app.log --pidfile $OPENSHIFT_TMP_DIR/uwsgi.pid
```

Edit `.openshift/action_hooks/stop` to the following:

```
    #!/bin/bash
    kill `cat $OPENSHIFT_TMP_DIR/uwsgi.pid`
```

### Deploy

Commit all of the changes to the repository:

`git commit -am 'initial commit'`

Deploy to OpenShift:

`git push`

You should now be able to browse and see your application running:

`curl http://py27-[username].rhcloud.com`

Should return:

    Hello from Flask

And to verify that your application is using Python 2.7:

`curl http://py27-[username].rhcloud.com/info`

Should return:

    2.7.3

