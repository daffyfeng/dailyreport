## 需求
自己项目需要mock一下数据，所以研究下vue中mock使用方式

## 方案

一开始看的vue2，特别简单

[在Vue-cli中使用mock.js](https://juejin.cn/post/6987080258126086157)

项目是vue3的，require在vite中使用不了，所以重新看

使用**vite-plugin-mock**

```javascript
import { defineConfig } from "vite";
import type { ConfigEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { viteMockServe } from "vite-plugin-mock";

// https://vitejs.dev/config/
export default ({ command }: ConfigEnv) => {
  // 可以在env中就行配置
  const prodMock = false;
  return defineConfig({
    plugins: [
      vue(),
      viteMockServe({
        mockPath: "./src/mock", // 设置模拟.ts 文件的存储文件夹
        localEnabled: command === "serve", // 设置是否启用本地 xxx.ts 文件，不要在生产环境中打开它.设置为 false 将禁用 mock 功能
        prodEnabled: command !== "serve" && prodMock, // 设置打包是否启用 mock 功能
        supportTs: true, // 打开后，可以读取 ts ⽂件模块。请注意，打开后将⽆法监视.js ⽂件。
        watchFiles: true, // 监视⽂件更改，并重新加载 mock 数据
        /* 如果生产环境开启了 mock 功能,即prodEnabled=true.则该代码会被注入到injectFile对应的文件的底部。默认为main.{ts,js}
      这样做的好处是,可以动态控制生产环境是否开启 mock 且在没有开启的时候 mock.js 不会被打包。
      如果代码直接写在main.ts内，则不管有没有开启,最终的打包都会包含mock.js
      */
        injectCode: `
        import { setupProdMockServer } from './mockProdServer';
        setupProdMockServer();
      `,
      }),
    ],
    ...
  });
};


```

[vite+vue3中vite-plugin-mock使用方式](https://www.jianshu.com/p/ca4f0dd4de13)

[vite+vue3引入mock模块配置](https://blog.csdn.net/lareinax5/article/details/125167162)