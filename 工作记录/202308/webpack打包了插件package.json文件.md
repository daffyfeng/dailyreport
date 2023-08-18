## webpack 打包了插件 package.json 文件

安全检查扫描到项目编译后代码中，包含了 ant-design-vue 的 package.json，认为其透露了依赖关系......要整改

所以只好研究 webpack 是如何将其打包进去的，首先项目中是全引入的 ant-design-vue

```js
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
```

可以确认的是这样引用 ant-design-vue，webpack 会去`node_modules/ant-design-vue`下找 package.json 文件，获取其依赖关系，同时发现其是被打入名为 app 的 bundle 的文件中

试了好多方法都不行

```js
// 使用copy-webpack-plugin插件忽略package.json或者重写package.json
// 拷贝文件
const CopyWebpackPlugin = require('copy-webpack-plugin');
{
    plugins: [
        // copy custom static assets
        new CopyWebpackPlugin([
            {
                from: 'node_modules/ant-design-vue/package.json',
                to: 'node_modules/ant-design-vue/package.json',
                // 忽略无效
                // globOptions: {
                //     ignore: ['**'],
                // },
                // 只有在dist/node_modules/ant-design-vue/创建一个空的package.json
                transform: => {
                    return ""
                }
            }
        ]),
    ]
    }

// 配置rule，依然不生效
{
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: 'vue-loader',
                exclude: /node_modules\/ant-design-vue\/package.json/,
            },
        ],
    },
}

// 还有使用externals、 ignorePlugin和noParse等等
```

**最后原因仍然不知道，后面有空再研究怎么打包的吧** ，修改了引入方式，改为按需引入 ant-design-vue 才成功

```node
// 使用babel-plugin-import
npm install babel-plugin-import --save-dev

// .babelrc or babel.config.js 文件中添加
{
  "plugins": [
    ["import", { "libraryName": "ant-design-vue", "libraryDirectory": "es", "style": "css" }] // `style: true` 会加载 less 文件
  ]
}

// main.js
import { Button } from 'ant-design-vue';
Vue.use(Button)
```
