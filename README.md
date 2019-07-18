
## Kubectl-Plugins

## Overview
Contains useful kubectl-plugins created as described [here](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/#writing-kubectl-plugins) in the Kubernetes documentation.  Other possibly useful plugins can be found on [github](https://github.com/topics/kubectl-plugins) as well.

## Current plugins

### KUBECTL-SECRETSAPPLY

#### Summary
This python script can be used as a kubectl plugin to convert K8s Secret manifests that contain plain-text secrets to the base64 equivalent and then immediately apply it to the cluster in one command.

NOTE: Ideally you would want to handle your secrets in a more organized secure automated manner (AWS Param Store, Hashicorp Vault, etc.), but this works well enough for POC or even in small environments if you are careful about cleanup of the original secret plain text source file.  One improvement might be to add the option to delete the original plain text secret (or even better) to only offer option to `not delete` it.  Either way, this can work as a nice example on what is possible with kubectl plugins.

#### Prereqs
 - You will need [PyYAML](https://pyyaml.org/) - install it if needed via pip `pip3 install pyyaml`
 - Python 3.5+  (tested on 3.7.3)

#### Installation
1. Rename the file to `kubectl-secretsapply` with *no* extension
2. Install the plugin by placing the renamed script anywhere in your PATH
   (assumes properly configured kubectlis also in PATH).  e.g. ~/bin etc

#### Usage
1. Create a yaml Secret using plaintext secrets (not encoded)
2. Execute `kubectl secretsapply mysecret-manifest-to-convert-and-apply.yaml` which will
   convert all the secrets to k8s compat base64 and immediately apply it to the
   cluster using kubectl and your current context.
3. Also runs `kubectl get` on the new secret for easy confirmation via CLI

#### Optional
If you do not want to use as a kubectl plugin, you can call the script as a normal python script `./kubectl-secretsapply <yourfile>`
