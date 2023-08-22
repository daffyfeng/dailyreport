## Cesium 添加自定义弹窗并跟随地图移动

有个需求，cesium 地图上添加站点，点击站点需要弹窗显示站点内容

思路：点击站点获取到站点位置，将其转换为 web 页面的位置，再显示弹窗内容即可

```js
let ray = viewer.camera.getPickRay(event.position);
cartesian = viewer.scene.globe.pick(ray, viewer.scene);
// 将WGS84坐标中的位置转换为窗口坐标
let windowPosition = Cesium.SceneTransforms.wgs84ToWindowCoordinates(
  viewer.scene,
  cartesian
);
```

```js
let cartesian; // 射线与地球表面之间的交点
// 绑定屏幕空间事件 全局点击事件
let handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
handler.setInputAction(function (event) {
  let pick = viewer.scene.pick(event.position);
  if (pick && pick.id.id) {
    document.getElementById("stateShow").style.display = "block";
    let ray = viewer.camera.getPickRay(event.position);
    cartesian = viewer.scene.globe.pick(ray, viewer.scene);
    document.getElementById("title").innerHTML = pick.id.data.title;
    document.getElementById("state").innerHTML = pick.id.data.state;
    document.getElementById("info").innerHTML = pick.id.data.info;
    // 实时更新位置
    viewer.scene.postRender.addEventListener(updatePosition);
  } else {
    document.getElementById("stateShow").style.display = "none";
    // 移除事件监听
    viewer.scene.postRender.removeEventListener(updatePosition);
  }
}, Cesium.ScreenSpaceEventType.LEFT_CLICK);

// 位置更新
function updatePosition() {
  // 将WGS84坐标中的位置转换为窗口坐标
  let windowPosition = Cesium.SceneTransforms.wgs84ToWindowCoordinates(
    viewer.scene,
    cartesian
  );
  // 数值是样式中定义的宽高
  if (windowPosition == undefined) return;
  document.getElementById("stateShow").style.left =
    windowPosition.x - 220 / 2 + "px";
  document.getElementById("stateShow").style.top =
    windowPosition.y - 150 + "px";
}
```

#### 参考

[Cesium 添加自定义弹窗并跟随地图移动](https://www.cnblogs.com/l-s-f/p/17160200.html)
