$(document).ready(function() {
    $("div.bhoechie-tab-menu>div.list-group>a").click(function(e) {
        e.preventDefault();
        $(this).siblings('a.active').removeClass("active");
        $(this).addClass("active");
        var index = $(this).index();
        $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
        $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
    });
});

$(document).ready(function() {
    $("#carouselExampleFade>.carousel-control-next").click(function(e) {
        e.preventDefault();
        var elemCount  = document.getElementsByClassName("carousel-inner")[0].childElementCount;
        console.log(elemCount);
        if ($('div.carousel-item.active').index() == elemCount - 1){
            var index = 0;
        }else {
            var index = $('div.carousel-item.active').index() + 1;}
        $("div.container>div.bhoechie-tab-content").removeClass("active");
        $("div.container>div.bhoechie-tab-content").eq(index).addClass("active");
    });
 $("#carouselExampleFade>.carousel-control-prev").click(function(e) {
        e.preventDefault();
        if ($('div.carousel-item.active').index() == -1){
            var index = 0;
        }else {
            var index = $('div.carousel-item.active').index() - 1;}
        $("div.container>div.bhoechie-tab-content").removeClass("active");
        $("div.container>div.bhoechie-tab-content").eq(index).addClass("active");
    });
});

