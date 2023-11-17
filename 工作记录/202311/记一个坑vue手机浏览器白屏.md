### vue手机浏览器上白屏

用之前的框架改了改，然后重写个新项目，项目写完，PC端完美运行

但是要去手机浏览器也要能运行，打开一看白屏

最开始怀疑是不是路由有问题，手机浏览器更严格点，试了在路由守卫里加日志，结果根本没反应
```js
router.beforeEach((to, from, next) => {
  alert(JSON.stringify(from));
  alert(JSON.stringify(to));
  next();
});
```

又看了下兼容性问题，vue自带babel降低版本，应该没问题的

代码里面引入了vconsle，调试看下到底哪出了毛病
```html
<script src="https://unpkg.com/vconsole@latest/dist/vconsole.min.js"></script>
  <script>
    // VConsole 默认会挂载到 `window.VConsole` 上
    var vConsole = new window.VConsole();
  </script>
```

发现console里面没有报错，最后发现访问站点，但是没有请求app.js

最后还是同事用ios调试，vconsole中才报错，提示Notication没有定义
```js
Vue.prototype.$notice = Notification;
```

这段代码是属于老框架的，确实是没有定义，注释之后就没问题了

### 安卓浏览器没有提示报错，ios提示报错，就离谱！！！！！！