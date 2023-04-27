XHR、Ajax、Axios 和 Fetch 都是用于在 web 应用程序中进行数据交互的技术。它们的共同点是可以通过 HTTP 请求从服务器获取数据，但是每种技术具有独特的特点和应用场景。

### 相同点

- 可以通过 HTTP 请求从服务器获取数据。
- 可以使用使用异步的方式进行数据请求和响应处理。
- 可以设置请求头、请求参数、响应拦截器等操作。

### 不同点

##### XHR

XMLHttpRequest（XHR）是原生的 JavaScript API，允许在不刷新页面的情况下发送 HTTP 请求和接收响应。XHR 可以手动配置请求头和请求参数，并且还可以实现进度监控。XHR 通常需要手动编写 Ajax 请求代码，因此开发成本相对较高。

##### Ajax

Ajax（Asynchronous JavaScript and XML）是一种基于 XHR 的前端开发技术，它使用 JavaScript 发送 HTTP 请求和接收响应。Ajax 可以更新部分页面而无需刷新整个页面，提高了用户体验。Ajax 是一种相对低级别的技术，需要手动编写大量的 JavaScript 代码。

##### Axios

Axios 是一个基于 Promise 的 HTTP 客户端，可以在浏览器和 Node.js 中使用。Axios 提供了简单易用的 API，支持并发请求、请求和响应拦截器、自动转换 JSON 数据等功能。Axios 适用于更为复杂的 HTTP 请求，例如上传和下载文件、处理流式数据等。

##### Fetch

Fetch 是一种原生的 JavaScript API，提供了一种简洁和灵活的方式来发送和接收 HTTP 请求。Fetch 使用 Promise 进行异步操作，可以使用一组简单的 API 将请求和响应构建成流水线。Fetch 兼容性良好，但需要手动管理错误处理、超时控制和请求拦截器等。
