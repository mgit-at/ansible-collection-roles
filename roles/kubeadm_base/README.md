kubeadm_base
============

Installs kubeadm, kubectl and haproxy.

Haproxy is used to provide the kubernetes API on every node on `localhost:6443` since load balancing GRPC connections seems to have its issues otherwise.

See https://github.com/kubernetes/kubeadm/blob/main/docs/ha-considerations.md for more info.

This role requires a proper inventory group layout and a few global variables to be set.
