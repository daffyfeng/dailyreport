## 方案
只需要在pdf路径后面加上#scrollbars=0&toolbar=0&statusbar=0即可去除工具栏

```javascript
<iframe :src="pdfUrl + '#scrollbars=0&toolbar=0&statusbar=0'" frameborder="0" width="100%" height="100%"></iframe>
```
> 参考
[浏览器预览pdf去除顶部工具栏](https://blog.csdn.net/lixin_labi/article/details/113242983)
[前端实现word、excel、pdf、ppt、mp4、图片、文本等文件的预览](https://juejin.cn/post/7071598747519549454#heading-5)