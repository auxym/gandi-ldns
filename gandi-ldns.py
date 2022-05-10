#!/usr/bin/env python3


# Standard library
import configparser
import os
import socket
import sys
from urllib.parse import urljoin

# Third-party
import requests


def get_zone_ip(section):
    """Get the current IP from the A record in the DNS zone"""

    endpoint = "domains/%s/records" % section["domain"]
    api_url = urljoin(section["api"], endpoint)

    ip = "0.0.0.0"

    resp = requests.get(api_url, headers={"X-Api-Key": section["apikey"]})
    resp.raise_for_status()

    current_zone = resp.json()
    name = section["a_name"]

    # There may be more than one A record - we're interested in one with
    # the specific name (typically @ but could be sub domain)
    for record in current_zone:
        if record["rrset_type"] == "A" and record["rrset_name"] == name:
            ip = record["rrset_values"][0]
            break

    return ip


def get_ip():
    """Get external IP"""

    try:
        # Could be any service that just gives us a simple raw
        # ASCII IP address (not HTML etc)
        resp = requests.get("https://api.ipify.org")
    except requests.exceptions.HTTPError:
        print("Unable to external IP address.")
        sys.exit(2)

    return resp.text


def change_zone_ip(section, new_ip):
    """Change the zone record to the new IP"""

    a_name = section["a_name"]
    domain = section["domain"]
    apikey = section["apikey"]

    endpoint = "domains/%s/records/%s/%s" % (domain, a_name, "A")
    api_url = urljoin(section["api"], endpoint)

    body = {
        "rrset_ttl": section.getint("ttl"),
        "rrset_values": [
            new_ip,
        ],
    }

    resp = requests.put(api_url, json=body, headers={"X-Api-Key": apikey})
    resp.raise_for_status()


def read_config(config_path):
    """Open the configuration file or create it if it doesn't exists"""
    if not os.path.exists(config_path):
        return None
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    return cfg


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir, "config.txt")
    config = read_config(path)
    if not config:
        sys.exit("please fill in the 'config.txt' file")

    for section in config.sections():
        zone_ip = get_zone_ip(config[section])
        current_ip = socket.gethostbyname(config.get(section, "host"))
        if current_ip == "127.0.0.1":
            current_ip = get_ip()

        if zone_ip.strip() == current_ip.strip():
            continue
        else:
            print(
                "DNS Mistmatch detected: A-record: ",
                zone_ip,
                " WAN IP: ",
                current_ip,
            )
            change_zone_ip(config[section], current_ip)
            zone_ip = get_zone_ip(config[section])
            print("DNS A record update complete - set to ", zone_ip)


if __name__ == "__main__":
    main()
