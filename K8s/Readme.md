
kubectl create pod --image=nginx --name my-pod  ---> POST call --> Kube api server

Kubeapi-server --> Entry in etcd 


{
    pod:{
        "absq21231s":{
            "name":"my-pod"
            "image":"nginx"
            "state":Pending
            "node":""
        }
    }
}


Scheduler: Rank Nodes and then assign a node to Pod


{
    pod:{
        "absq21231s":{
            "name":"my-pod"
            "image":"nginx"
            "state":Pending
            "node":"Node1"
        }
    }
}

kubelet will fetch the metadata and give instructions to CRI to create the containers.

Kubelet sends the data back to etcd 

{
    pod:{
        "absq21231s":{
            "name":"my-pod"
            "image":"nginx"
            "state":Running
            "node":"Node1"
        }
    }
}




Replicasets



Multi container patters.

Init Container Pattern:
    2 containers 
    Init container -- one time job
    App container -- running
    Ex: 
    My app is a backend api server and it relies on a database for running.
    Init container - Small service that gets completed only when database is up.

Sidecar Container Pattern:
    2 containers
    sidecar -- running
    app container -- running
    ex: Running a log transport application with your main app

Adapter Container Pattern
    2 container
    adapter container -- running
    app container -- running
    It converts the data to the type the main app understands

Ambassador Pattern
    2 container
    ambassador -- running
    app container -- running
    It usually works as a proxy, kind of prevents our main container to talk to external endpoints directly
    It is helpful in security as it helps you do SSL/TLS Termination for the app container

    nginx (listens on port 443), does the SSL termination (with certificates) transfers all the api call on port 443 to port 80 of main app.



Create -- only create resources (fails if resource exists)
Apply -- can create and update resources
