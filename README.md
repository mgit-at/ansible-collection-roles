# mgIT roles Collection for Ansible
[![CI](https://github.com/mgit-at/ansible-collection-roles/workflows/CI/badge.svg?event=push)](https://github.com/mgit-at/ansible-collection-roles/actions)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mgit-at/ansible-collection-roles/main.svg)](https://results.pre-commit.ci/latest/github/mgit-at/ansible-collection-roles/main)

<!-- no Codecov (yet?) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/REPONAMEHERE)](https://codecov.io/gh/ansible-collections/REPONAMEHERE) -->

This collection contains common roles in active use by mgIT GmbH.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.
This is obvioulsy NOT a repository under the `ansible_community` GitHub organization, so please get in touch with mgIT GmbH instead of raising a complaint with the Ansible Community team.
Still you can expect your complaint to be treated very similarly.

## Communication

Releases etc. are announced on GitHub in this repository (https://github.com/mgit-at/ansible-collection-roles) and Issues, PRs etc. are the intended main communication channel.

If you need to communicate in private, you can contact us via the "Contact" section on [our homepage](https://mgit.at/).

## Contributing to this collection

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Governance

This collection is maintained and provided by mgIT GmbH.
It is in active daily use, so in the end the deciding factor will be if a proposed change helps in our daily work.
External views and contributions are of course very valuable to have and we appreciate feedback, BUT this is not a community project or a democracy (just to set no wrong expectations).

## Tested with Ansible

This collection is intended to be used with `ansible-core>=2.10`.
It only contains roles (which are a bit harder to test than plugins/modules).

## External requirements

Any external requirements are documented in the roles themselves.

## Included content

### roles/base

Role to set up the base configuration of an Ubuntu/Debian server.
Intended to be run against a clean installation with only a default `sshd` running and access to an up-to-date mirror.

### roles/kubernetes/...

Bundle of roles that are intended to be run in sequence to set up a minimal production ready Kubernetes cluster.
The setup is highly opinionated (OS: latest Ubuntu LTS with HWE kernel, installation: kubeadm, CRI: containerd, CNI: Cilium) and not expected to support a lot of options in the future.

## Using this collection

TODO: Create tests and refer as usage example (likely requires actual VMs, not containers...).

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install mgit_at.roles
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: mgit_at.roles
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install mgit_at.roles --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install mgit_at.roles:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/REPONAMEHERE/tree/main/CHANGELOG.rst).

## Roadmap

Start publishing roles that are in common use internally or that are required for the MVP "set up a k8s cluster with public roles".

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [mgIT Website](https://mgit.at/)
## Licensing

Apache-2.0 License

See [LICENSE](LICENSE) to see the full text.

Copyright 2021 mgIT GmbH.
