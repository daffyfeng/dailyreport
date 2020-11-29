$(function () {
    var $carousels = $('.carousel');
    $carousels.carousel({interval: 4000})
    var startX,endX;
    var offset = 50;
    $carousels.on('touchstart',function (e) {
        startX = e.originalEvent.touches[0].clientX;
        $carousels.carousel('pause');
    });
    $carousels.on('touchmove',function (e) {
        endX = e.originalEvent.touches[0].clientX;
    });
    $carousels.on('touchend',function (e) {
    	$carousels.carousel({interval: 4000})
        var distance = Math.abs(startX - endX);
        if (distance > offset){
            $(this).carousel(startX >endX ? 'next':'prev');
        }
    }) 
});


var mySwiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    paginationClickable: true,
    autoplay:3000,
    onSlideChangeEnd:function(data){
        var prev = data.previousIndex;
        var index = data.activeIndex;
        $(".banner .checked").removeClass("checked");
        $(".banner .title").eq(index).addClass("checked");
    },
    onInit:function(){
        this.onSlideChangeEnd({activeIndex:0});
    }
});
//鼠标覆盖停止自动切换
mySwiper.container[0].onmouseover=function(){
  mySwiper.stopAutoplay();
}
//鼠标移出开始自动切换
mySwiper.container[0].onmouseout=function(){
  mySwiper.startAutoplay();
}