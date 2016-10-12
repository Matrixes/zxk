/*
通过检查变量myBookmarklet是否已定义来发现bookmarklet是否已经加载。
这样做的目的是: 如果用户重复点击bookmarklet，就可以避免再次加载。

如果myBookmarklet没有定义，我们就为DOM添加一个<script>标签，来加载bookmarklet.js,
并且使用一个随机数作为参数，以避免从浏览器缓存中加载。

真正的bookmarklet代码在bookmarklet.js中，这样做的目的是：不需要用户更新他们之前添加到
浏览器的bookmark， 我们就可以修改bookmark代码。

将bookmlet初始化器添加到用户个人中心界面
*/
(function(){
	if (window.myBookmarklet !== undefined) {
		myBookmarklet();
	} else {
		document.body.appendChild(document.createElement('script')).src='http://127.0.0.1:8000/static/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
	}
}) ();