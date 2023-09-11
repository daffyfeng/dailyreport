## 页面经过transform缩放页面后elementui tooltip偏移问题

之前有个需求，页面不管怎么缩放，页面内容都要保持不变。
最后采用了body元素上使用`transform:scale()`的方式来实现

element-ui: '^2.15.1'

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

正常情况下，已经没有问题了。但是element-ui有部分组件是渲染在body组件下的，此时会自己计算元素所在位置的left、top等属性

`<el-table>`组件中`<el-table-column>`有个属性`showOverflowTooltip`置为true时，对于cell内容width超过分配的width时，自动展示一个`<el-tooltip>`

展示的tooltip渲染在body下，鼠标移动到cell上时，position:fixed，同时计算出left，top等。此时scale发生变化，就会出现偏移


试了很多方式（appendToBody等）都不行，只有翻源码了

```js
// table-body.js中整个tbody下添加el-tooltip组件
// <el-tooltip effect={this.table.tooltipEffect} placement="top" ref="tooltip" content={this.tooltipContent}></el-tooltip>

// table-column.js中判断showOverflowTooltip属性，存在则在cell上添加class
if (column.showOverflowTooltip) {
            props.class += ' el-tooltip';
            props.style = {width: (data.column.realWidth || data.column.width) - 1 + 'px'};
          }

// table-body.js中给cell添加mouseEnter监听，判断是否展示tooltip
handleCellMouseEnter(event, row) {
      ...

      // 判断是否text-overflow, 如果是就显示tooltip
      const cellChild = event.target.querySelector('.cell');
      if (!(hasClass(cellChild, 'el-tooltip') && cellChild.childNodes.length)) {
        return;
      }
      ...

      if ((rangeWidth + padding > cellChild.offsetWidth || cellChild.scrollWidth > cellChild.offsetWidth) && this.$refs.tooltip) {
        const tooltip = this.$refs.tooltip;
        // TODO 会引起整个 Table 的重新渲染，需要优化
        this.tooltipContent = cell.innerText || cell.textContent;
        tooltip.referenceElm = cell;
        tooltip.$refs.popper && (tooltip.$refs.popper.style.display = 'none');
        tooltip.doDestroy();
        tooltip.setExpectedState(true);
        this.activateTooltip(tooltip); // 展示tooltip，
      }
    }
// 

// tooltip/src/main.js 中 showPopper置为true
// 其mixins了Popper(/utils/vue-popper.js)，而
// Popper中又引入了popper.js
const PopperJS = Vue.prototype.$isServer ? function() {} : require('./popper');


// vue-popper.js中监听了showPopper属性，更新时会触发updatePopper()

updatePopper() {
      const popperJS = this.popperJS;
      if (popperJS) {
        popperJS.update();
        if (popperJS._popper) {
          popperJS._popper.style.zIndex = PopupManager.nextZIndex();
        }
      } else {
        this.createPopper();
      }
    },

    // popperJS的update方法会执行runModifiers
    Popper.prototype.update = function () {
    ...

    // compute the popper and reference offsets and put them inside data.offsets
    data.offsets = this._getOffsets(
      this._popper,
      this._reference,
      data.placement
    );

    ...

    data = this.runModifiers(data, this._options.modifiers);

    if (typeof this.state.updateCallback === "function") {
      this.state.updateCallback(data);
    }
  };

// runModifiers会执行一个applyStyle方法,tooltip的left、top是在这写入的，可以看到left是来自data.offsets.popper，上面的代码可以发现是在update中通过_getOffsets方法获取的
Popper.prototype.modifiers.applyStyle = function (data) {
    ...

    // round top and left to avoid blurry text
    var left = Math.round(data.offsets.popper.left);
    var top = Math.round(data.offsets.popper.top);

    ...
      styles.left = left;
      styles.top = top;
    
    ...
    
    Object.assign(styles, data.styles);

    setStyle(this._popper, styles);

    ....
  };

// 是通过reference和popper两个元素获取的，这两个分别是父级元素（鼠标滑动到的那个元素）和tootip元素本身，通过getBoundingClientRect获取位置大小进行计算
Popper.prototype._getOffsets = function (popper, reference, placement) {
    ...

    //
    // Get reference element position
    //
    var referenceOffsets = getOffsetRectRelativeToCustomParent(
      reference,
      getOffsetParent(popper),
      isParentFixed
    );

    //
    // Get popper sizes
    //
    var popperRect = getOuterSizes(popper);

    ...

    
    popperOffsets.left =
    referenceOffsets.left +
    referenceOffsets.width / 2 -
    popperRect.width / 2;
    if (placement === "top") {
    popperOffsets.top = referenceOffsets.top - popperRect.height;
    } else {
    popperOffsets.top = referenceOffsets.bottom;
    }
    

    // Add width and height to our offsets object
    popperOffsets.width = popperRect.width;
    popperOffsets.height = popperRect.height;

    return {
      popper: popperOffsets,
      reference: referenceOffsets,
    };
  };

// getBoundingClientRect方法，在body整个scale缩放后，获取到的值都是缩放后的；
// 而页面直接缩放后，getBoundingClientRect获取的值不会改变，偏移就是这样产生的，解决的方法只有重新计算

// vue-popper.js初始化时, 会去获取popperOptions中onUpdate，如果这个属性是方法，
// 就会将其添加到this.state.updateCallback上，这个方法在update执行时也会跟着执行，而且是在runModifiers后
createPopper() {
      ...
      const options = this.popperOptions;
      ...

      if (typeof options.onUpdate === 'function') {
        this.popperJS.onUpdate(options.onUpdate);
      }
      ...
    },

 Popper.prototype.onUpdate = function (callback) {
    this.state.updateCallback = callback;
    return this;
  };

// <el-tooltip>中有popper-options这个设置项，传入一个function，修改popper.left top即可
data: {
  ...
  popperOptions: {
    boundariesPadding: 10,
    gpuAcceleration: false,
    onUpdate: this.onUpdateTooltip
  }
},
methods: {
  onUpdateTooltip(data) {
    console.log(data);

    const { _popper } = data.instance
    const { popper, reference } = data.offsets

    const ele = document.documentElement.querySelector("body")
    const transform = ele.style.transform
    const position = /\(.*\)/.exec(transform)[0].replace('(', '').replace(')', '').split(',')
    // body上设置了transform: scale(xx, xx)
    const scaleX = Number(position[0]), scaleY = Number(position[1])
    // 参照_getOffsets方法，还原reference的位置数据重新计算
    _popper.style['left'] = Math.round(reference.left / scaleX + (reference.width / scaleX) / 2 - popper.width / 2) + 'px'
    _popper.style['top'] = Math.round(reference.top / scaleY - popper.height) + 'px'
  },
}
```

