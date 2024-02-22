## 描述

代码

```html
<div class="content-bg">
    <el-scrollbar ref="scrollbar2" class="scrollMenuBox">
        <div class="content">
            <div class="detail" v-for="(item, i) in clickedThing.detail"
                :key="i">
                <!-- 内容 -->
            </div>
        </div>
    </el-scrollbar>
</div>
```

```css
.content{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
}
```

content使用弹性布局，数据横向增加，同时固定高度。期望数据量超过固定宽度后产生横向滚动条。

### 结论

```js
this.$post('xxxxx', { }).then((data) => {
    this.$set(this.clickedThing, 'detail', data)
    this.$nextTick(() => {
        // 使用nextTick同时，手动触发滚动条update方法
        this.$refs.scrollbar2.update()
    })
})


```

### 遇到的坑

通过直接修改调试页面scrollMenuBox中的宽度，取消其宽度，横向滚动条就能展示。

查看页面发现是横向滚动条的属性发生了改变，增加了width

```html
<div class="el-scrollbar__bar is-horizontal">
    <div class="el-scrollbar__thumb" style="transform: translateX(0%);width: 78.9%">
    </div>
</div>
```

翻看源码找到，发现是滚动条创建时，**获取到滚动条区域的clientWidth和scrollWidth比例来产生的width属性，如果相同则不会有滚动条出现**

```js
// element-ui/packages/scrollbar/src/src/main.js
nodes = ([
        wrap,
        <Bar
          move={ this.moveX }
          size={ this.sizeWidth }></Bar>,
        <Bar
          vertical
          move={ this.moveY }
          size={ this.sizeHeight }></Bar>
      ]);

update() {
      debugger
      let heightPercentage, widthPercentage;
      const wrap = this.wrap;
      if (!wrap) return;

      heightPercentage = (wrap.clientHeight * 100 / wrap.scrollHeight);
      widthPercentage = (wrap.clientWidth * 100 / wrap.scrollWidth);

      this.sizeHeight = (heightPercentage < 100) ? (heightPercentage + '%') : '';
      this.sizeWidth = (widthPercentage < 100) ? (widthPercentage + '%') : '';
    }


// element-ui/packages/scrollbar/src/src/bar.js
return (
      <div
        class={ ['el-scrollbar__bar', 'is-' + bar.key] }
        onMousedown={ this.clickTrackHandler } >
        <div
          ref="thumb"
          class="el-scrollbar__thumb"
          onMousedown={ this.clickThumbHandler }
          style={ renderThumbStyle({ size, move, bar }) }>
        </div>
      </div>
    );

// element-ui/packages/scrollbar/src/src/util.js

export function renderThumbStyle({ move, size, bar }) {
  const style = {};
  const translate = `translate${bar.axis}(${ move }%)`;

  style[bar.size] = size;
  style.transform = translate;
  style.msTransform = translate;
  style.webkitTransform = translate;

  return style;
};
```

于是加日志准备看下渲染时是啥情况，运行的源码是在element-ui中lib目录下的，找到lib/scrollbar.js文件，找到对应代码，增加log输出。

坑的地方就出现了，打印的滚动条不是我要调试的这个，而是页面其他滚动条，就懵圈了

通过各种加日志，最后查看编译后的代码，才发现scrollbar有两套代码的，生成的dist文件中，搜索出了两套scrollbar代码，一套里面有加的各种日志，另一套还是原来的，此时确定scroller是用这套代码渲染出来的。

最后才发现另一套代码在lib/element-ui.common.js中

**为啥没有一开始就直接搜索出两套代码，是因为vscode搜索时，不知道为啥打开了排除文件，导致只在打开的文件中进行搜索，下次切记切记，因为这个耽误了很长时间**

