> /usr/local/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --cgroup-driver=systemd --network-plugin=cni --pod-infra-container-image=dockerhub.kubekey.local/kubesphereio/pause:3.5 --node-ip=x.x.x.31 --hostname-override=master1

这段命令是用来启动 Kubernetes 节点上的 kubelet 服务的。下面是各参数的解释：

> - /usr/local/bin/kubelet：kubelet 二进制文件的路径。
> - --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf：指定 kubelet 使用的 bootstrap kubeconfig 文件的路径，该文件用于 kubelet 向 kube-apiserver 注册节点信息，并获取证书和密钥等信息以授权与集群通信。
> - --kubeconfig=/etc/kubernetes/kubelet.conf：指定 kubelet 使用的 kubeconfig 文件的路径，该文件包含 kubelet 与其它组件（如 kube-apiserver、kube-controller-manager、kube-scheduler）进行通信所需的配置信息。
> - --config=/var/lib/kubelet/config.yaml：指定 kubelet 使用的配置文件的路径，该文件包含 kubelet 本身的配置选项，例如 pod 资源限额、容器运行时等。
> - --cgroup-driver=systemd：指定 kubelet 使用的 cgroup driver，即容器的资源限制工具，默认为 cgroups。这里设置为 systemd，表示使用 systemd 来管理容器资源。
> - --network-plugin=cni：指定 kubelet 使用的网络插件类型，即容器网络的实现方式。这里设置为 cni，表示使用 CNI（Container Network Interface）规范的网络插件。
> - --pod-infra-container-image=dockerhub.kubekey.local/kubesphereio/pause:3.5：指定 kubelet 使用的 Pod 基础设施容器的镜像地址和版本号。Pod 基础设施容器包含了 Pause 容器和 kubelet-helper 等辅助程序，用于实现 Kubernetes Pod 的生命周期管理。
> - --node-ip=x.x.x.31：指定节点的 IP 地址。
> - --hostname-override=master1：指定节点的主机名。
>   综上，以上启动 kubelet 服务的命令是按照指定参数进行配置后，以指定参数值作为 kubelet 服务运行的参数进行启动的。

##有个需求，kubesphere 服务中需要获取用户真实 ip，但是 kubesphere 内部会使用集群转发，实例中获取到的请求 ip 地址是内部转发地址

##yml 文件中修改 externalTrafficPolicy 值为 Local，配置后服务就无法使用集群内部转发，服务内部可以获取客户端访问的真实 ip
