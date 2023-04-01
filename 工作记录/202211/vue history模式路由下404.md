## 起因
遇到个问题，vue路由`history`模式下，访问`/xxx/login`直接nginx 404

根据官方文档，vue启动`history`模式，路由中就能去掉#
```javascript
new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  });
```

改成这样之后，问题出现了
访问`/xxx/login`，显示nginx的404的页面

## 分析

查看network中访问记录，发现`/xxx/login`，没有命中/index.html
访问`localhost:5002`时，命中了/index.html

这个时候想起以前另外一个项目上有试过history，记得上可以实现的，而且两个项目的框架应该是同一个。
然后就疯狂查看两个项目的区别，事实证明记忆这种东西是不准确的，之前的项目改成`history`后，是可以自动跳转，但是刷新就404，查看network一样的不会命中\index.html



耗费大量时间比对两个项目不同点后，发现没有乱用

重新换个思路
怀疑是vue-cli启动的server里面，路由判定有问题
就开始翻vue@cli-server源码，翻到/lib/commands/serve.js
发现启动的是**WebpackDevServer**
```javascript
const server = new WebpackDevServer(compiler, Object.assign({
      ...
      historyApiFallback: {
        disableDotRule: true,
        rewrites: genHistoryApiFallbackRewrites(options.publicPath, options.pages)
      }
      ...
})
)

server.listen(port, host, err => {
    if (err) {
        ...
    }
})

function genHistoryApiFallbackRewrites (baseUrl, pages = {}) {
  const path = require('path')
  const multiPageRewrites = Object
    .keys(pages)
    // sort by length in reversed order to avoid overrides
    // eg. 'page11' should appear in front of 'page1'
    .sort((a, b) => b.length - a.length)
    .map(name => ({
      from: new RegExp(`^/${name}`),
      to: path.posix.join(baseUrl, pages[name].filename || `${name}.html`)
    }))
  return [
    ...multiPageRewrites,
    { from: /./, to: path.posix.join(baseUrl, 'index.html') }
  ]
}
```

**genHistoryApiFallbackRewrites**方法中返回值中，添加了默认路由，匹配不到时，就转到index.html，但是很明显这玩意儿没有生效(后面才知道是还没到它生效的时候就返回来了404)


继续翻WebpackDevServer到源代码，

```js
class Server {
    constructor(compiler, options = {}, _log) {
        if (options.lazy && !options.filename) {
            throw new Error("'filename' option must be set in lazy mode.");
        }
        ...
        // 创建express
        this.setupApp();
        ...
        // 加载各种中间件，包含webpack-dev-middleware、http-proxy-middleware、connect-history-api-fallback
        this.setupFeatures();
        ...
    }

    setupApp() {
        // Init express server
        // eslint-disable-next-line new-cap
        this.app = new express();
    }
    

    setupFeatures() {
        const features = {
            proxy: () => {
                if (this.options.proxy) {
                    this.setupProxyFeature();
                }
            },
            historyApiFallback: () => {
                if (this.options.historyApiFallback) {
                    this.setupHistoryApiFallbackFeature();
                }
            },
            middleware: () => {
                // include our middleware to ensure
                // it is able to handle '/index.html' request after redirect
                // 使用 webpack-dev-middleware
                this.setupMiddleware();
            },
            ...
        }

        ...

        const runnableFeatures = [];

        ...

        runnableFeatures.push('setup', 'before', 'headers', 'middleware');

        ...
        // 调试发现注释掉这段就能正常访问到`/xxx/login`，但是代理失效
        // 验证码都加载不出来
        if (this.options.proxy) {
            runnableFeatures.push('proxy', 'middleware');
        }

        ...

        if (this.options.historyApiFallback) {
            runnableFeatures.push('historyApiFallback', 'middleware');
        }

        ...
        
        // 中间件加载顺序 middleware -> proxy -> historyApiFallback
        (this.options.features || runnableFeatures).forEach((feature) => {
            features[feature]();
        });

    }

    setupMiddleware() {
        this.app.use(this.middleware);
    }
}

```
将这段代码注释调，就能实现命中/index.html
```js
if (this.options.proxy) {
    runnableFeatures.push('proxy', 'middleware');
}
```
原因就很明显了，代理导致的这个问题，但是代理注释掉后，访问api就gg了
```js
module.exports = {
    publicPath: process.env.NODE_ENV === "production" ? "/" : "/",
    outputDir: 'dist',
    assetsDir: 'static',
    // eslint-loader 是否在保存时检查
    lintOnSave: false,
    productionSourceMap: false,
    devServer: {
        publicPath: '/',
        host: 'localhost',
        port: 5002,
        overlay: {
            warnings: false,
            errors: true
        },
        proxy: {
            [process.env.VUE_APP_BASE_API]: {
                target: "http://xxxxxx:13001", 
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    ['^' + process.env.VUE_APP_BASE_API]: ''
                }
            },
        }
    },
    ...
}
```
### 解决方法

因为我们项目中**process.env.VUE_APP_BASE_API**一直配置的是'/'，这会导致所有请求（页面、资源以及api）都经过代理
hash模式时，访问url为`http://localhost:5002/#/xxxx/login`时，不会命中代理，会先返回/index.html

history模式时，访问url为`http://localhost:5002/xxxx/login`时，会命中代理，直接访问`target/xxxx/login`，返回当然是404了

这个时候只需要修改下**process.env.VUE_APP_BASE_API**即可，改成'/api'
(内心是我了个大草的)
改成'/api'后，`/xxxx/login`就不会走代理了，完美（-_-）

试了下确实没问题了，不过出现了一个新问题

由于我的url是`/xxx/login`，所以访问验证码地址从`/auth` -> `/xxx/auth`

懵逼了都，在控制台手写**XMLHttpRequest**，访问的地址也是`/xxx/auth`

百度回来解决方案，设置axios的baseURL
```js
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API
});
```

然后又又又有问题了，打包放到服务器，nginx转发出毛病了，依然404
这个好解决，加上`try_files $uri $uri/ /index.html;`
找不到文件的时候，默认指向index.html
vue是单页应用，只有index.html这一个页面，路由调整都是vue自己控制的，无需nginx转发，返回index.html就完事了

注意生产环境时，VUE_APP_BASE_API可以不用改为/api，不用修改以前的nginx配置，只需要按照上诉方法修改即可

```nginx
location / {
    root   xxxx\xxxx;
    try_files $uri $uri/ /index.html;
    index  index.html index.htm;
}
```

### 补充

为啥hash模式就不会用到代理，history就会用到，后面再翻了下代码
发现是`webpack-dev-middleware`造成的，也就是上面的代码`this.setupMiddleware();`使用的中间件

hash模式时，req.url值为/，#后面的内容没有算到url中，filename补上index.html，执行最后的res.send(context)，返回index.html的内容

history模式时，req.url值为`/xxx/login`，找不到`/xxx/login`这个文件或者文件夹，会发生异常，执行goNext()，执行后面的代理中间件，被代理转到`target`/xxx/login``，发生404
```js
module.exports = function wrapper(context) {
  return function middleware(req, res, next) {
        function goNext() {
            ...
            next()
            ...
        }
        ...

        let filename = getFilenameFromUrl(
            context.options.publicPath,
            context.compiler,
            req.url
        );

        if (filename === false) {
            return goNext();
        }
        ...
         return new Promise((resolve) => {
            handleRequest(context, filename, processRequest, req);
            // eslint-disable-next-line consistent-return
            function processRequest() {
                try {
                    let stat = context.fs.statSync(filename);
                    if (!stat.isFile()) {
                        if (stat.isDirectory()) {
                            let { index } = context.options;

                            // eslint-disable-next-line no-undefined
                            if (index === undefined || index === true) {
                                index = 'index.html';
                            } else if (!index) {
                                throw new DevMiddlewareError('next');
                            }

                            filename = path.posix.join(filename, index);
                            ...
                        }
                    }
                } catch (e) {
                    return resolve(goNext());
                }

                // server content
                let content = context.fs.readFileSync(filename);
                ...
                res.send(content);
                ...
            }
        }
    }
}
```

### 参考
[浅析npm run serve命令](https://blog.csdn.net/qq_31772441/article/details/119941900)
[WebpackDevServer实现请求转发以及解决单页面应用路由问题](https://blog.csdn.net/qq_39207948/article/details/113832349)
[vue-路由history模式刷新页面404及上线后的代理问题](https://blog.csdn.net/RequesToGod/article/details/126284395)