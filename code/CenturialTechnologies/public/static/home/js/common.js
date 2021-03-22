// scroll
// $(window).scroll(function(){
// 	var top = $(window).scrollTop();
// 	if(top>200){
// 		$("#head").css("background","rgba(0, 0, 0, 1)");
// 	}else{
// 		$("#head").css("background","rgba(0, 0, 0, 0.27)");
// 	}

// })
// seach
$(".glyphicon-search").click(function(){
	if(/on/.test($(".searchInput").attr("class"))){
		search($(".searchInput").val());
	}else{
		$(".searchInput").addClass("on").focus();
	}
})
$('.searchInput').bind('keypress',function(event){ 
    if(event.keyCode == 13) {  
         search($('.searchInput').val());  
     }  
 });
function search(q){
	window.open("serach.html?q="+q);
}
// menu
$("#menu .exit").click(function(){
		$("#menu").removeClass("menuIn").slideUp();
	})
	$("#head .menuOpen").click(function(){
		$("#menu").addClass("menuIn").slideDown();
	})
	$('#collapseOne').on('hide.bs.collapse', function () {
	  $("#menu .zk").addClass("no");
	})
	$('#collapseOne').on('show.bs.collapse', function () {
	  $("#menu .zk").removeClass("no");
	})