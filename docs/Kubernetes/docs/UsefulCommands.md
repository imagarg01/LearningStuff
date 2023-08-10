## Kubectl Commands

```cmd
# Create a resource from a file or from stdin.
kubectl create -f FILENAME

# Expose a resource as a new Kubernetes service.
kubectl expose rc nginx --port=80 --target-port=8000
```


```cmd
#List all services in namespace
kubectl get services 


# List all pods in all namespaces
kubectl get pods --all-namespaces


# List all pods in the namespace
kubectl get pods
```

```cmd
# Describe commands with verbose output
kubectl describe nodes my-node
kubectl describe pods my-pod
```

```cmd
# dump pod logs (stdout)
kubectl logs my-pod  

# Run pod as interactive shell
kubectl run -i --tty busybox --image=busybox:1.28 -- sh

# Start a single instance of nginx pod in the namespace of mynamespace
kubectl run nginx --image=nginx -n mynamespace
```
