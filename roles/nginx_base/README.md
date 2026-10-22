nginx_base
==========

This role installs nginx from the distribution, with mgIT's base config,
snippets and a systemd override that always restarts nginx.

Migrating away from ppa:ondrej/nginx
------------------------------------

ppa:ondrej/nginx was deleted upstream in 2026-04 (last series 1.28.x, see
https://codeberg.org/oerdnj/deb.sury.org/issues/67). The role removes the ppa
source, key and pin, but fails while nginx from the ppa is still installed:
swapping the packages takes nginx down, so it is done by hand.

Before you start:

- Check that the config works with the distro nginx (Ubuntu 22.04 ships 1.18,
  24.04 ships 1.24): `nginx -T` must not use newer directives, e.g.
  `ssl_reject_handshake` (>= 1.19.4, disable `nginx_base_ssl_reject_handshake_enabled`)
  or `http2 on;` (>= 1.25.1).
- Ubuntu's `nginx-extras` has no lua module from 24.04 on. Hosts with
  `*_by_lua*` directives need another solution first (e.g. openresty).
- Remove the ppa source by hand before running any playbook: every role that
  updates the apt cache fails on the deleted ppa, and nginx_base often runs late.

Migration (nginx is down between steps 3 and 4, so download first):

1. Remove the ppa source and pin:
   `rm /etc/apt/sources.list.d/nginx.sources /etc/apt/preferences.d/nginx && apt update`
2. Download the Ubuntu packages (use your `nginx_base_pkg_variant`; the ppa
   builds are newer, so name the version from `apt-cache policy nginx-extras`):
   `apt-get install --download-only --allow-downgrades nginx-extras=1.24.0-2ubuntu7.18`
3. Remove (don't purge, that keeps /etc/nginx) the ppa packages:
   `apt remove $(dpkg-query -W -f '${Package} ${Version}\n' | awk '$1 ~ /^(nginx|libnginx-mod-|lua-resty-|libluajit-5\.1-)/ && $2 ~ /deb\.sury\.org/ {print $1}')`
4. Install the Ubuntu packages without letting their scripts start nginx; nginx
   would start before the module packages are configured and fail on module
   directives such as `more_set_headers`:
   `printf '#!/bin/sh\nexit 101\n' > /usr/sbin/policy-rc.d && chmod 755 /usr/sbin/policy-rc.d`,
   `apt install nginx-extras`, then `rm /usr/sbin/policy-rc.d`
5. Remove links of ppa-only modules (lua, ndk) that were not restored:
   `rm -f /etc/nginx/modules-enabled/*.conf.removed`
6. `nginx -t && systemctl restart nginx`, then run the role.

Don't downgrade in place (pin + `--allow-downgrades`): on 22.04 the ppa and
Ubuntu ship `/usr/sbin/nginx` in different packages, and dpkg deletes it.
