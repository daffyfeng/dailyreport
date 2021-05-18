var mySwiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    paginationClickable: true,
    prevButton:'.swiper-button-prev',
    nextButton:'.swiper-button-next',
    autoHeight: true,
    setWrapperSize: true,
    autoplay: 3000,
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
