Base Role
=========

This role installs basic packages and does basic system hardening.

To use specific ssh configuration set the flag:
```
base_sshd_extended_conf: true
```

PCP: `dstat` is a transitional package for `pcp` on Ubuntu >= 24.04 and Debian >= 13, which
starts several collector daemons and timers. `base_pcp_mode` controls them:
```
base_pcp_mode: disabled   # default: stop and mask all PCP daemons and timers, dstat keeps working
base_pcp_mode: unmanaged  # leave PCP alone (does not unmask units masked earlier)
```
The PCP tasks are tagged `base_pcp`.

Documentation and testing is still a work in progress.
