## 页面经过transform缩放页面后elementui tooltip偏移问题

之前有个需求，页面不管怎么缩放，页面内容都要保持不变。
最后采用了body元素上使用`transform:scale()`的方式来实现

```js
// 全局监听orientationchange|size事件，通过获取doc.documentElement的大小，
// 拿到一个缩放比（预设页面大小是1920*929），然后修改body元素上transform属性，
// 实现反向缩放，保持页面不变

const resizeEvt = "orientationchange" in window ? "orientationchange" : "resize"
const recalc = () => {
    const docEl = doc.documentElement;
    const { width, height } = docEl.getBoundingClientRect();
    const app = docEl.querySelector("body");
    app.style.transform = `scale(${(width / 1920).toFixed(6)})`;
}
window.addEventListener(resizeEvt, recalc, false);
```

