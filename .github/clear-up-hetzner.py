from hcloud import Client
import os
from datetime import datetime, timedelta, timezone
import timeago

client = Client(token=os.environ['HCLOUD_TOKEN'])

MAGIC_SSH_KEY = "allow-deletion-script"

assert client.ssh_keys.get_by_name(MAGIC_SSH_KEY), (
    f"This hetzner cloud project does not have the magic ssh-key named '{MAGIC_SSH_KEY}', refusing to delete anything..."
)

# Two days ago from now in UTC
two_days_ago = datetime.now(timezone.utc) - timedelta(days=2)
now = datetime.now(timezone.utc)

print("deleting servers and keys older than 2 days...")

for server in client.servers.get_all():
    if server.created < two_days_ago:
        print(f"Server {server.name} is being deleted, it was created {timeago.format(server.created, now)}...")
        client.servers.delete(server)

for ssh_key in client.ssh_keys.get_all():
    if ssh_key.name == MAGIC_SSH_KEY:
        continue
    if ssh_key.created < two_days_ago:
        print(f"SSH-Key {ssh_key.name} is being deleted, it was created {timeago.format(ssh_key.created, now)}...")
        client.ssh_keys.delete(ssh_key)
