from interfaces2networkd import (
    parse_network_config,
    config_to_interface_definitions,
    definitions_to_systemd_networkd,
    render_systemd_files,
)


def _test_snapshot(snapshot, prefix, file_content):
    snapshot.snapshot_dir = "pytest_snapshot/interfaces2networkd"
    # Not sure if we need everything snapshotted
    result = parse_network_config(file_content)
    snapshot.assert_match(str(result), f"snapshot_{prefix}_config")
    intf = config_to_interface_definitions(result)
    snapshot.assert_match(str(intf), f"snapshot_{prefix}_interfaces")
    files = definitions_to_systemd_networkd(intf)
    snapshot.assert_match(str(files), f"snapshot_{prefix}_files")
    rendered = render_systemd_files(files)
    snapshot.assert_match(str(rendered), f"snapshot_{prefix}_rendered")


def test_hetzner_vm(snapshot):
    file_content = """
### Hetzner Online GmbH installimage

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback
iface lo inet6 loopback

auto ens3
iface ens3 inet dhcp

iface ens3 inet6 static
  address 2a01:4f8:c012:d80c::2
  netmask 64
  gateway fe80::1
  dad-attempts 0
    """
    _test_snapshot(snapshot, "hetzner_vm", file_content)


def test_hetzner_root(snapshot):
    file_content = """
### Hetzner Online GmbH installimage

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback
iface lo inet6 loopback

auto eth0
iface eth0 inet static
  address 5.9.41.140
  netmask 255.255.255.224
  gateway 5.9.41.129
  # route 5.9.41.128/27 via 5.9.41.129
  up route add -net 5.9.41.128 netmask 255.255.255.224 gw 5.9.41.129 dev eth0

iface eth0 inet6 static
  address 2a01:4f8:161:308e::2
  netmask 64
  gateway fe80::1
  dad-attempts 0
    """
    _test_snapshot(snapshot, "hetzner_root", file_content)
