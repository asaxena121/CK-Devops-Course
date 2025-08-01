# CK-Devops-Course


Network Drivers

Bridge -- Connects all the containers connected to the same bridge network ( We can acess other containers by their container name)

host -- Containers uses the host machine's network as their own

Null -- No network connection (isolated network)



container orchestration tool -- docker swarm

swarm  --- bees swarm (group)

node - host machine,ec2 server or something with compute capabilities
m1,m2,m3 --- nodes
m1               m2                 m3            m4        m5          ....... m100
docker          docker          docker 
c1,c2           c3,c4           c5,c6
...100          ..100           ..20
                                c211


docker swarm

manager node        --   manage, create container(assign workload) also runs containers (default behaviour is : manager is also a worker)
worker node         --  run containers(services or tasks)

you can have multiple manager nodes and ofcourse multiple worker nodes


best practice: always have more than 3 manager nodes (high availability) but the recommended number is 7 (if 3 workers fail there will be atleast 4 running)


services -- keep on running
task -- job (runs and gets completed)


                                      c1
                    c2   
                            c3
            0.l x                     c4                       
manager == worker  worker  worker   worker 
(0.5x)        2x    2x      2x        2x




Overlay Network

Connect containers spanned across multiple hosts/node




local machine : public 10.2.4.2
(manager)




Docker buildx vs buildkit\



local runner (ec2)

Github --> Pull main --> kubeconfig  -> kubectl apply -f 

devs -->
app-dev cluster
app-dev-code github

ArgoCD
Github (PR merge) --> Kubernetes cluster


deployment ()
