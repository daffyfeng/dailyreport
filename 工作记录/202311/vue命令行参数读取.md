### 需求

项目中很多页面，但是每次打包只能打包其中一个页面同时还得修改路由指向该页面，就非常麻烦
就想着能够通过命令行输入页面名称，自动打包项目同时router指向该文件

```sh
npm run serve --appName=aaaaa
npm run build --appName=aaaaa
```

```js
// 修改package.json
{
"scripts": {
    "serve": "node checkAppName.js && vue-cli-service serve",
    "build": "node checkAppName.js && vue-cli-service build",
    }
}

// 增加checkAppName.js

const appName = process.env.npm_config_appName;
if (!appName) {
  console.error(
    "必须填写appName参数, 参数内容参见/src/appConfig.js, 格式为npm run serve --appName=xxxx"
  );
  process.exit(1); // 终止进程并返回非零退出码
}

// vue中process.env只能有VUE_APP开头的参数, 所以修改vue.config.js
process.env.VUE_APP_NAME = process.env.npm_config_appName; // 将参数设置到环境变量中

// 修改router.js
// 值得注意点一点，import不支持变量写入，只支持这种`${path}`不能是`${appConfig[appName]}`

const appName = process.env.VUE_APP_NAME || "";
const { path, title } = appConfig[appName];
// 路由懒加载
const Home = () =>
  import(/* webpackChunkName: "home" */ `../views/${path}.vue`);

```