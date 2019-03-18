<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="css/index.css" />
<title>Insert title here</title>
<script type="text/javascript" src="js/jquery-1.11.0.min.js"></script>
<script type="text/javascript" src="js/json2.js"></script>
<script>
$(document).ready(function() {
	refreshLogin();
});
function refreshLogin(){
	 var userName = '<%= session.getAttribute("userName")%>';
     console.log("userName:::" + userName);
     if(userName!="null"){
    	 $("#login_message").text("欢迎"+userName);
    	 $("#login_message").removeAttr("href");
    	 $("#register").parent().remove();
    	 var li_fav='<li><a id="favorite" href="${pageContext.request.contextPath}/favorite">收藏夹</a><li>'
         $("ul").append(li_fav);
    	 var li_exit = $('<li><a id="exit" href="${pageContext.request.contextPath}/login_exit">退出</a></li>');
    	 $("ul").append(li_exit);
     }
}
</script>
</head>
<body>
	<div class="menu">
			<ul>
				<li>
					<a id="login_message" href="${pageContext.request.contextPath}/loginForm">登录</a>
				</li>
				<li>
					<a id="register" href="${pageContext.request.contextPath}/registerForm">注册</a>
				</li>
			</ul>
	</div>
		<form action="${pageContext.request.contextPath}/literature/litList"
		method="GET" target="_blank">
		
		<div id="search" align="center">
			<input id="keyWord" name="keyWord" type="text"> 
			<input id="sub_bt" type="submit" value="查询文献">
		</div>
	</form>
</body>
</html>