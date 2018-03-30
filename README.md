gandi-ldns
==========

Simple quick & dirty script to update DNS A record of your domain dynamically
using gandi.net's API.  It is very similar to no-ip and dyndns et al where you
can have a domain on the internet which points at your computer's IP address,
except it is free (once you have registered the domain) and does not suffer
from any forced refreshing etc.

This fork is originally based on 
[matt1's gandi-ddns script](https://github.com/matt1/gandi-ddns), however, it
it modified to use Gandi's new "LiveDNS" API instead of the old XML-RPC API. 
The major differences are:

* Uses the LiveDNS API and therefore requires your LiveDNS API key, which is
  different from the XML-RPC key.

* Only retains compatibility with Python 3.3+, as Python 2.7 will be officially
  retired in 2020.

* Dependent on the excellent [Requests](http://docs.python-requests.org/)
  library.

This version is mostly compatible with the original config file format,
only the API Key and API URL need to be changed (see `config.example.txt`).

Every time the script runs it will get the current domain config from
gandi.net's API and look for the IP in the A record for the domain (default
name for the record is '@' but you can change that if you want to).  It will
then get your current external IP from a public "what is my ip" site.  Once it
has both IPs it will compare what is in the DNS config vs what your IP is, and
update the DNS config for the domain as appropriate so that it resolves to your
current IP address.

Setup
--------------

Ensre you have Python 3.3+ installed, as well as Requests. If you are running
a Linux distribution, Requests can likely be installed from your distribution's
repositories.

On Arch-based distributions:

```sh
pacman -S python-requests
```

On Debian-based distributions (Ubuntu, Mint, etc):

```sh
apt install python3-requests
```

Then, simply download/clone the contents of this repository to a location
of your choice.

You should then copy `config.example.txt` to `config.txt` and, at a minimum,
modify the values for `domain` and `apikey`. If you want to edit the DNS
record for a subdomain, you should also edit the `a_name` entry.

Usage
-----------

The script can be simply ran as `python3 gandi-ldns.py` and takes no arguments. The
config.txt file in the script folder will be used.

To run periodically, you can use cron or systemd timers.
