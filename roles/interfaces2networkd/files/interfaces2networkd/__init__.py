#!/usr/bin/env python3

# This has been implemented as a tool so it can be used in environments like
# during a hetzner install or just as a general standalone tool

from types import SimpleNamespace
from ipaddress import ip_interface, ip_address
import argparse
from argparse import Namespace
from typing import Iterator, Tuple
import os


def parse_network_config(file_content):
    # Split the input content into lines
    lines = file_content.strip().splitlines()

    # Initialize an empty list to store the parsed configuration blocks
    parsed_configs = []

    # Temporary storage for each configuration
    current_config = None
    parsing = False

    for line in lines:
        # Start parsing when line starts with "iface"
        if line.startswith("iface"):
            if current_config:
                parsed_configs.append(current_config)
            current_config = {}
            parts = line.split()
            if len(parts) != 4:
                raise Exception("invalid intf definition '%s'" % line)

            current_config["intfname"] = parts[1]
            current_config["family"] = parts[2]
            current_config["type"] = parts[3]
            parsing = True

        # If parsing is ongoing and line starts with two spaces, it's a parameter
        elif parsing and line.startswith("  "):
            param = line.strip()
            if param:
                key, value = param.split(" ", 1)
                current_config[key.replace("-", "")] = value

        # If the line does not start with two spaces, finish parsing
        elif parsing:
            parsed_configs.append(current_config)
            current_config = {}
            parsing = False

    # Append any remaining config (in case it ends without a non-parameter line)
    if current_config:
        parsed_configs.append(current_config)

    return parsed_configs


def config_to_interface_definitions(result):
    intf = {}

    # Print the result
    for config_ in result:
        config = SimpleNamespace(**config_)

        # ignore loopback, as systemd-networkd always creates it
        if config.intfname == "lo":
            continue

        if config.intfname not in intf:
            intf[config.intfname] = {}

        res = SimpleNamespace(
            **{
                "dhcp": False,
                "gw": None,
                "cidr": None,
                "dad": True,
                "peergw": False,
            }
        )

        if config.type == "static":
            # this normalizes 255.255... to cidr
            if "/" in config.address:
                res.cidr = str(ip_interface(config.address))
            else:
                res.cidr = str(
                    ip_interface(("%s/%s" % (config.address, config.netmask)))
                )
            res.gw = str(ip_address(config.gateway))
            if "dadattempts" in config_:
                res.dad = config.dadattempts != "0"
            # hetzner static address for ipv4 has custom script to add gw as peer
            # (gw is outside of cidr, so it won't find it otherwise)
            if "up" in config_:
                res.peergw = True
        elif config.type == "dhcp":
            res.dhcp = True
        else:
            raise Exception("Unknown type %s" % config.type)

        if config.family == "inet6":
            intf[config.intfname]["v6"] = res
        elif config.family == "inet":
            intf[config.intfname]["v4"] = res
        else:
            raise Exception("Unknown interface family %s" % config.family)

    return intf


# NOTE: always use read_mac=True if possible.
# (requires this script to run on the same machine that the config is from)
def definitions_to_systemd_networkd(intfs, read_mac=False):
    files = {}

    for intf, intfv in intfs.items():
        match = {}
        network = {
            "Address": [],
            "Gateway": [],
        }
        address = []

        def common(v):
            if not v.dhcp:
                # TODO: handle dad
                if v.peergw:
                    address.append({"Address": v.cidr, "Peer": v.gw})
                # NOTE: dad also exists on ipv4 in networkd (!)
                elif not v.dad:
                    address.append(
                        {"Address": v.cidr, "DuplicateAddressDetection": "none"}
                    )
                else:
                    network["Address"].append(v.cidr)

                network["Gateway"].append(v.gw)

        if "v4" in intfv:
            common(intfv["v4"])
        if "v6" in intfv:
            common(intfv["v6"])
        if "v4" in intfv and intfv["v4"].dhcp and "v6" in intfv and intfv["v6"].dhcp:
            network["DHCP"] = "yes"
        elif "v4" in intfv and intfv["v4"].dhcp:
            network["DHCP"] = "ipv4"
        elif "v6" in intfv and intfv["v6"].dhcp:
            network["DHCP"] = "ipv6"
        else:
            network["DHCP"] = "no"

        if read_mac:
            with open(f"/sys/class/net/{intf}/address") as f:
                match["MACAddress"] = f.read().strip()
        else:
            match["Name"] = intf

        files["40-%s.network" % intf] = {
            "Match": match,
            "Network": network,
            "Address": address,
        }

    return files


def listify(v):
    if isinstance(v, list):
        return v
    else:
        return [v]


def render_systemd_files(files):
    out = {}

    def render_systemd_file(content):
        for section, scontent in fcontent.items():
            for content in listify(scontent):
                yield "[%s]" % section
                for k, v in content.items():
                    for vv in listify(v):
                        yield "%s=%s" % (k, vv)
                yield ""

    for name, fcontent in files.items():
        out[name] = "\n".join(render_systemd_file(fcontent))

    return out


def process(file_content, read_mac=False):
    # Parse the content
    result = parse_network_config(file_content)
    intf = config_to_interface_definitions(result)
    files = definitions_to_systemd_networkd(intf, read_mac)
    rendered = render_systemd_files(files)

    return rendered


def parse_arguments() -> Tuple[Namespace, list[str]]:
    """Parse given command line arguments."""
    parser = argparse.ArgumentParser(
        description="interfaces2networkd",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--by-name",
        action="store_true",
        help="Reference the interface by name instead of by mac",
    )
    parser.add_argument("--chroot", type=str, help="Path to chroot", default="/")
    return parser.parse_known_args()


def main():
    args, params = parse_arguments()

    interfaces = os.path.join(args.chroot, "etc", "network", "interfaces")
    output = os.path.join(args.chroot, "etc", "systemd", "network")

    if len(params) == 2:
        interfaces = params[0]
        output = params[1]

    content = ""
    with open(interfaces, "r", encoding="utf-8") as f:
        content = f.read()

    intf_d = interfaces + ".d"
    if os.path.isdir(intf_d):
        for filename in os.listdir(intf_d):
            file_path = os.path.join(intf_d, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content += f.read()

    rendered = process(content, not args.by_name)

    for file, content in rendered.items():
        with open(os.path.join(output, file), "w+") as f:
            f.write(content)


if __name__ == "__main__":
    main()
