kubeadm_controlplane
====================

Will run slightly different depending on which node type this is running on.

On an "initial control plane node", it will run `kubeadm init`, then install Cilium using `helm`, on all "other control plane nodes" it will run `kubeadm join`.
It will also set up a kubeconfig for the root user.

Remember: We already have haproxy running, so the "global" API-server will always be on `127.0.0.1:6443`, but the actual API server on control plane nodes needs to run on port `6442` so haproxy picks it up.
