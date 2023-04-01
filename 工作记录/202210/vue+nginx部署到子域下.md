## 需求

新项目需要部署到源项目子域 A.com/workflow 下

## 方案
查看vue.config文档，修改publicPath，改为 '/workflow'，
```javascript
module.exports = {
    publicPath: process.env.NODE_ENV === "production" ? "/workflow" : "/",
    outputDir: 'dist/workflow',
}
```
同时修改router的base地址
```javascript
export default new Router({
  mode: 'history', 
  scrollBehavior: () => ({ y: 0 }),
  base: '/workflow',
  routes
})
```
这样生产环境下，所有访问地址前都会加上前缀/workflow

修改nginx配置文件
```nginx

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
   
    server {
        listen       8219;
        server_name  localhost;
        
        location ^~/workflow/ {
            root D:\02_code\xxxx\dist;
            index  /workflow/index.html;
            try_files $uri $uri/ /workflow/index.html;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
```

### 参考
[vue router使用history模式发布nginx的打包配置](https://blog.csdn.net/xlt_jbwkj/article/details/124836668)
[vue（1）-配置（1）publicpath、nginx、vue-router的base](https://blog.csdn.net/qq_42440919/article/details/121922183)