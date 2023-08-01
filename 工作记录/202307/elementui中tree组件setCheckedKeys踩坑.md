## 起因

为了图方便，tree 数据保存时，如果父级节点勾选了，则只存入父级节点数据。
前端展示时，利用 tree 组件特性，自动将子级节点选中

## 踩坑

前端展示时，增加了一个只读模式，所以 tree 需要设置 disabled。问题就出现了，所有节点 disabled 都设置为 true 时，
**setCheckedKeys()** 只能选中叶子节点
disabled 的时候，tree 组件将节点之间的交互给停了

源码

```js
setChecked(value, deep, recursion, passValue) {
    this.indeterminate = value === 'half';
    this.checked = value === true;

    if (this.store.checkStrictly) return;

    if (!(this.shouldLoadData() && !this.store.checkDescendants)) {
      let { all, allWithoutDisable } = getChildState(this.childNodes);

      // 这个地方会将父级节点给取消选中all为false  allWithoutDisable 为true
      if (!this.isLeaf && (!all && allWithoutDisable)) {
        this.checked = false;
        value = false;
      }
......

export const getChildState = node => {
  let all = true;
  let none = true;
  let allWithoutDisable = true;
  for (let i = 0, j = node.length; i < j; i++) {
    const n = node[i];
    if (n.checked !== true || n.indeterminate) {
      all = false;
      if (!n.disabled) {
        allWithoutDisable = false;
      }
    }
    if (n.checked !== false || n.indeterminate) {
      none = false;
    }
  }

  return { all, none, allWithoutDisable, half: !all && !none };
};
```

## 解决

筛了一遍数据，将所有 checked 的节点都拿出来，父级节点选中则需要将所有子级节点 key 都拿出来
