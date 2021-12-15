kubeadm_master
==============

Will run slightly different depending on which node type this is running on.

On a "primary master", it will run `kubeadm init`, on all "secondary masters" it will run `kubeadm join`.
Afterwards it will set up a kubeconfig for the root user on the node and install Cilium using `helm`.

Remember: We already have haproxy running, so the "global" API-server will always be on `127.0.0.1:6443`, but the actual API server needs to run on port `6442` so haproxy picks it up.
