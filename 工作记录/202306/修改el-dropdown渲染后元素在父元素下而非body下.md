### 参考

- [ElementUI 中解决使用 dropdown 等弹窗时定位 body 而非 template 创建的 dom 节点](https://blog.csdn.net/DDD4V/article/details/122944358)

dropdown

```js
<el-dropdown>
    <el-dropdown-menu slot="dropdown" :append-to-body="false">
        <el-dropdown-item></el-dropdown-item>
    </el-dropdown-menu>
</el-dropdown>
```
通过el-dropdown-menu组件中appendToBody参数解决该问题

先写到这
