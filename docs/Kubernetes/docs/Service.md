## Introduction


Service provides abstraction to a set of pods available on the network so that clients can interact with it.
Each Service object defines a logical set of endpoints (usually these endpoints are Pods) along with a policy about how 
to make those pods accessible.

The set of Pods targeted by a Service is usually determined by a **selector** that you define.
- Load balancing for pods
- Use labels to determine target pods

A service is a Kubernetes resource that:
- provide layer-4 load balancing for a group of pods
- service discovery using the cluster's internal DNS.

## Defining s Service

Sample yaml of a service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

It creates a new Service named "my-service" with the default ClusterIP service type. The Service targets TCP port 9376 on any Pod with the "app.kubernetes.io/name: MyApp" label.


## Types of Services

1. ClusterIP Service

Cluster IP Services are used for communication between Pods within the same Kubernetes cluster.
The Service gets exposed on a static IP that's unique within the cluster. When you make a request to that IP, the 
Service takes care of redirecting the traffic to one of the Pod's. 

**ClusterIP Services are meant for Pod-to-Pod communication only. They are not accessible from outside the cluster.**

User for internal-facing services
- a virtual IP address that load balances requests to a set of backend pods
- accessible anywhere within the cluster
- not externally accessible


2.  Node Port

Exposes the Service on each Node's IP at a static port (the NodePort). To make the node port available, Kubernetes sets up a cluster IP address, the same as if you had requested a Service of type: ClusterIP.

3. Load Balancer

Exposes the Service externally using an external load balancer. Kubernetes does not directly offer a load balancing component; you must provide one, or you can integrate your Kubernetes cluster with a cloud provider.

4. External Name

Maps the Service to the contents of the externalName field (for example, to the hostname api.foo.bar.example). The mapping configures your cluster's DNS server to return a CNAME record with that external hostname value. 


## Service Networking

