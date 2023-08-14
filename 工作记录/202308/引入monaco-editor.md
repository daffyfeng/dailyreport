## 引入 monaco-editor

项目需要，需要引入一个 json 文件的富文本编辑器，翻了下项目代码，发现很久以前引入过 monaco-editor

直接使用发现有个问题，无法格式化，控制台报错`Unexpected usage at EditorSimpleWorker.loadForeignModule`

加载不了插件

反复研究发现是安装 monaco-editor 安装版本太老了，更新下版本即可

```javascript
// 第一步
npm install monaco-editor@0.28.1 monaco-editor-webpack-plugin@4.2.0 --save
// 第二步 vue.config.js 增加配置
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = {
  chainWebpack (config) {
    config.plugin('monaco').use(new MonacoWebpackPlugin())
  }
}
```

主动触发格式化方法如下

```js
editor.setValue(this.value);
editor.trigger("", "editor.action.formatDocument"); //自动格式化代码
editor.setValue(editor.getValue()); //再次设置
```
