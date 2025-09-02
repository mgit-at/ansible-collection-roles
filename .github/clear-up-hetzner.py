from hcloud import Client
import os
from datetime import datetime, timedelta, timezone
import timeago

client = Client(token=os.environ['HCLOUD_TOKEN'])

MAGIC_SSH_KEY = "allow-deletion-script"

assert client.ssh_keys.get_by_name(MAGIC_SSH_KEY), (
    f"This hetzner cloud project does not have the magic ssh-key named '{MAGIC_SSH_KEY}', refusing to delete anything..."
)

# 6 hours ago from now in UTC - github runner timeout
oldest_allowed = datetime.now(timezone.utc) - timedelta(hours=6)
now = datetime.now(timezone.utc)

print(f"deleting servers and keys older than {timeago.format(oldest_allowed, now)}...")

for server in client.servers.get_all():
    if server.created < oldest_allowed:
        print(f"Server {server.name} is being deleted, it was created {timeago.format(server.created, now)}...")
        client.servers.delete(server)

for ssh_key in client.ssh_keys.get_all():
    if ssh_key.name == MAGIC_SSH_KEY:
        continue
    if ssh_key.created < oldest_allowed:
        print(f"SSH-Key {ssh_key.name} is being deleted, it was created {timeago.format(ssh_key.created, now)}...")
        client.ssh_keys.delete(ssh_key)
