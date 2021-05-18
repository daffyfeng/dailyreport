
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

var hash = window.location.hash
if (hash){
	$(hash).addClass('active').siblings().removeClass('active');
	$(".solution .d-none").eq($(hash).index()).addClass('active').siblings().removeClass('active');
}

$(".mb-container .node").click(function(){
	
	var index = $(this).index();
	if (index === 0){
		window.open('./solution.html#system_integration', '_self')
	}

	if (index === 1){
		window.open('./solution.html#data_center', '_self')
	}

	if (index === 2){
		window.open('./solution.html#intelligent_building', '_self')
	}

	if (index === 3){
		window.open('./solution.html#holographic_projection', '_self')
	}
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