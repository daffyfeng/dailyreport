
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

$(".solution .card").click(function(){
	$(this).addClass('active').siblings().removeClass('active');
	$(".solution .d-none").eq($(this).index()).addClass('active').siblings().removeClass('active');
})



$("#product").click(function(){
	window.open('./solution.html')
})

$("#wownow").click(function(){
	window.open('https://e.huawei.com/en/products/network-energy/dc-facilities/ids2000')
})

$("#peninsula").click(function(){
	window.open('https://zkteco.com/en/scheme_detail/9.html')
})