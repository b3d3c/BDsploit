# BDsploit

BDsploit (Big Data Exploitation and Post-exploitation Toolkit) is a series of scripts use to exploit and gain access on DC/OS and Marathon clusters. It also provides the ability to use Shodan API to search on the internet for exploitable clusters.

Please, only use this code if you can exploit a cluster

## Installation

Create virtualenv:
~~~~
virtualenv -p python3 «env_name» && cd «env_name»
~~~~

Activate virtualevn:
~~~~
source bin/activate
~~~~

Clone this project:
~~~~
git clone https://github.com/ebdecastro/BDsploit && cd BDsploit
~~~~

Install requirements:
~~~~
pip3 install -r requirements.txt
~~~~

Copy configuration file and edit it:
~~~~
cp conf_template.ini conf.ini
~~~~

Script must be run as root:
~~~~
sudo su
source ../bin/activate
python3 bdsploit.py
~~~~

## Requirements
It is neccessary to install [pupy](https://github.com/n1nj4sec/pupy) to use C&C capabilities.

## License
This code is under BSD 3-Clause license.
