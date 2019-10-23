# assault

A simple CLI load testing tool.

## Installation

Install using `pip`:

```
$ pip install assault
```

## Usage

The simplest usage of `assault` requires only a URL to test against and 500 requests synchronously (one at a time). This is what it would look like:

```
$ assault https://example.com
.... Done!
--- Results ---
Successful requests     500
Slowest                 0.010s
Fastest                 0.001s
Average                 0.003s
Total time              0.620s
Requests Per Minute     48360
Requests Per Second     806
```

If we want to add concurrency, we'll use the `-c` option, and we can use the `-r` option to specify how many requests that we'd like to make:

```
$ assault -r 3000 -c 10 https://example.com
.... Done!
--- Results ---
Successful requests     3000
Slowest                 0.010s
Fastest                 0.001s
Average                 0.003s
Total time              2.400s
Requests Per Minute     90000
Requests Per Second     1250
```

If you'd like to see these results in JSON format, you can use the `-j` option with a path to a JSON file:

```
$ assault -r 3000 -c 10 -j output.json https://example.com
.... Done!
```

### DocTest

Define tests within each method in class. Doctest uses the docstring to execute in the REPL
```
python -m doctest assault/stats.py
```


## Development

For working on `assault`, you'll need to have Python >= 3.7 (because we'll use `asyncio`) and [`pipenv`][1] installed. With those installed, run the following command to create a virtualenv for the project and fetch the dependencies:

Specific to RHEL7.6
```
sudo -i
export REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt
/opt/rh/rh-python36/root/usr/bin/pip3.6 install pipenv --proxy http://158.230.101.98:8080
pipenv install --python /opt/rh/rh-python36/root/usr/bin/python3.6 twine --dev
git init
git config --global user.name "Your Name"
git config --global user.email "Your Email Address"
git add --all
git commit -m "Initial Code Directory Commit"
git config credential.helper store
git remote add https://github.com/etc
# Workspace contains Pipfile but 'pipenv' was not found. Make sure 'pipenv' is on the PATH.
sudo ln -s /opt/rh/rh-python36/root/usr/bin/pipenv /usr/local/bin/pipenv
# pipenv install black --dev --pre # Installed Automatically - This is the pep8 auto-formatter
pipenv install pylint --dev
```

```
$ pipenv install --dev
...
```

Next, activate the virtualenv and get to work:
```
$ pipenv shell
...
(assault) $
```
> Remove the pipenv environment to rebuild: `pipenv --rm and rebuilding the virtual environment may resolve the issue.`
> `pipenv install --python /usr/local/bin/python3.7 twine --dev`

[1]: https://docs.pipenv.org/en/latest/

#### Install Package you are developing into virtualenv list of packages using setup.py
Update `setup.py`
```
entry_points={"console_scripts": ["assault=assault.cli:cli"]},
```
This installs the `package` into the `virtualenv` of current directory so application can be referenced by name instead of running like this: `python assault/cli.py -r 1 -c 2 http://www.google.com`
```
pip install -e .

Installing collected packages: assault
  Running setup.py develop for assault
Successfully installed assault
```
Run the Package using `assault`
```
(assault-ofeDDYAU) ✔ soula:assault [ master ✭ | ✚ 5 …2 ] ➭ assault --help
Usage: assault [OPTIONS] URL

Options:
  -r, --requests INTEGER     Number of requests
  -c, --concurrency INTEGER  Number of concurrent requests
  -j, --json-file TEXT       Path to output JSON file
  --help                     Show this message and exit.
```

#### Python 3.7 Install Procedure
```
sudo -i
yum groupinstall -y "Development Tools"
yum install -y zlib-devel
cd /usr/src
wget https://python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations --with-ensurepip=install
make altinstall
exit
```
> The make altinstall command prevents the built-in Python executable from being replaced.

Debian/Ubuntu Install
```
sudo -i
apt update -y
apt install -y \
  wget \
  build-essential \
  libffi-dev \
  libgdbm-dev \
  libc6-dev \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  libncurses5-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev

cd /usr/src
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar xf Python-3.7.3.tar.xz
cd Python-3.7.3.tar.xz
./configure --enable-optimizations --with-ensurepip=install
make altinstall
exit
```

Make sure secure_path in the /etc/sudoers file includes /usr/local/bin. The line should look something like this:
```
Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin
```

Upgrade PIP
```
sudo pip3.7 install --upgrade pip
```