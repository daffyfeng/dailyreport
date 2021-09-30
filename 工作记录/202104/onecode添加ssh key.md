


使用ed25519创建密钥，原因如下

    常见的 SSH 登录密钥使用 RSA 算法。RSA 经典且可靠，但性能不够理想。

    只要你的服务器上 OpenSSH 版本大于 6.5（2014 年的老版本），就可以利用 Ed25519 算法生成的密钥对，减少你的登录时间。如果你使用 SSH 访问 Git，那么就更值得一试。

    Ed25519 的安全性在 RSA 2048 与 RSA 4096 之间，且性能在数十倍以上。

## 准备工具 ssh-keygen

这个东西linux一般都有了，而我使用的是windows
安装Git for windows，里面包含了ssh-keygen

## 生成密钥

    # 创建并进入~/.ssh目录,ssh-keygen生成的密钥是在当前
    # 目录生成的，所以需要先进入。windows下
    # C:\Users\xxx\.ssh\
    mkdir -p ~/.ssh && cd ~/.ssh
    # 我在 GitHub
    ssh-keygen -t ed25519 -f my_github_ed25519  -C "me@github"
    # 我在 Gitee
    ssh-keygen -t ed25519 -f my_gitee_ed25519   -C "me@gitee"
    # 我在 GitLab
    ssh-keygen -t ed25519 -f my_gitlab_ed25519  -C "me@gitlab"
    # 我在企业
    ssh-keygen -t ed25519 -f my_company_ed25519 -C "email@example.com"

> **注意，上诉语句执行时让你填密码。如果你填了以后每次git拉取push都需要输入密码**

## 添加到配置文件

不同host代码仓库，想用不同邮箱操作时，可以通过配置文件进行处理

将常用 SSH 信息写进全局配置文件，省得连接时配置。

vi ~/.ssh/config 文件：

    # 关于别名
    # Host 是别名，HostName 是真正的域名。
    # 得益于别名，你可以直接以别名访问地址。例如：
    # 无别名： git clone git@github.com:torvalds/linux.git
    # 有别名： git clone github:torvalds/linux.git
    # 本例中使用与域名一致的别名，以免错误的配置导致登录不上。

    # 关于代理
    # SOCKS 代理格式： ProxyCommand connect -S localhost:1080  %h %p
    # HTTP 代理格式： ProxyCommand connect -H localhost:1080  %h %p
    ## SSH 代理依赖外部程序，这里使用了 Git for Windows 同捆的 connect.exe。
    ## Linux 下使用该代理方式需要额外安装 connect-proxy。

    # 我在 GitHub
    #  Host github.com
    #  Hostname github.com
    #  ProxyCommand connect -H localhost:1080  %h %p
    #User git
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/my_github_ed25519

    # 我在企业
    Host example.com
    #  Hostname example.com
    #  Port 22
    #  User git
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/my_company_ed25519


## 解释： ssh-keygen 的命令含义

    ssh-keygen -t rsa -b 4096 -f my_id -C "email@example.com"

其中：

+ [-t rsa] 表示使用 RSA 算法。
+ [-b 4096] 表示 RSA 密钥长度 4096 bits （默认 2048 bits）。Ed25519 算法不需要指定。
+ [-f my_id] 表示在【当前工作目录】下生成一个私钥文件 my_id （同时也会生成一个公钥文件 my_id.pub）。
+ [-C "email@example.com"] 表示在公钥文件中添加注释，即为这个公钥“起个别名”（不是 id，可以更改）。

在敲下该命令后，会提示输入 passphrase，即为私钥添加一个“解锁口令”。

##参考 
+ <https://zhuanlan.zhihu.com/p/110413836>
+ <https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>

