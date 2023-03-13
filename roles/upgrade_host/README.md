upgrade_host
============

NOT IDEMPOTENT!

This role applies upgrades via apt, reboots the host and then checks via systemd if it is still running correctly (again).
