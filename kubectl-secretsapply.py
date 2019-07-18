#!/usr/bin/env python3
"""
kubectl-secretsapply

SUMMARY
This python script can be used as a kubectl plugin to convert K8s Secret
manifests that contain plain-text secrets to the base64 equivalent
and then immediately apply it to the cluster in one command.

INSTALLATION
1. Rename the file to 'kubectl-secretsapply' with *no* extension
2. Install the plugin by placing the renamed script anywhere in your PATH
   (assumes properly configured kubectlis also in PATH).  e.g. ~/bin etc

USAGE
1. Create a yaml Secret using plaintext secrets (not encoded)
2. Execute `kubectl secretsapply mysecret-manifest.yaml` which will
   convert all the secrets to k8s compat base64 and immediately apply it to the
   cluster using kubectl and your current context.
3. Also runs `kubectl get` on the new secret for easy confirmation via CLI

OPTIONAL
If you do not want to use as a kubectl plugin, you can call the
script as a normal python script `./kubectl-secretsapply <yourfile>`

"""
import yaml
import sys
import base64
import subprocess
import tempfile


def main():
    """Main()."""
    try:
        if (len(sys.argv) != 2):
            raise ValueError("ERROR: You must provide the Kubernetes yaml Secret to convert/apply")

        with open(sys.argv[1], "r") as secret_file:
            contents = yaml.load(secret_file)
            dest_namespace = contents["metadata"]["namespace"]
            dest_name = contents["metadata"]["name"]
            is_secretfile = (True if contents["kind"] == "Secret" else False)
            if not is_secretfile:
                raise ValueError("ERROR: This is not a Kubernetes manifest of kind 'Secret'!")

            for key, val in contents["data"].items():
                contents["data"][key] = base64.b64encode(bytes(val, 'utf-8'))

        # Apply the config to the cluster
        with tempfile.NamedTemporaryFile(mode='w') as temp_file:
            yaml.dump(contents, temp_file, default_flow_style=False)
            apply_completed = subprocess.run(["kubectl", "apply", "-f",
                                            temp_file.name, "--record"], stdout=subprocess.PIPE, encoding="utf8")
            print(apply_completed.stdout)

        # Echo back the encoded k8s secret as confirmation
        get_completed = subprocess.run(["kubectl", "get", "secrets", dest_name, "-n", dest_namespace,
                                    "-o", "yaml"], stdout=subprocess.PIPE, encoding="utf8")
        print(get_completed.stdout, end='')
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
