$(document).ready(function () {

    $("#navbar-btn").on("click",function () {

        if ($("#sidebar-nav").css("left") == "0px") {
            $("#sidebar-nav").animate({"left": '-260px'});
            hideMask();
            $("body").css({"overflow":"scroll",
                "overflow-y":"auto"});
        } else {
            $("#sidebar-nav").animate({"left": '0px'});
            showMask();
            $("body").css({"overflow":"scroll",
            "overflow-y":"hidden"});
        }
    });
    $("#mask").on("click",function () {
        $("#sidebar-nav").animate({"left": '-260px'});
        hideMask();
        $("body").css({"overflow":"scroll",
            "overflow-y":"auto"});
    });
    //
    // $(window).scroll(function() {
    //     // console.info($(window).scrollTop());
    //     if($(window).scrollTop()==0){
    //         $(".navbar-default").css({"background-color":"transparent"});
    //     }else{
    //         $(".navbar-default").css({"background-color":"#3f51b5"});
    //     }
    // });
    // $(".icon-submenu").parent("a").click(function(){
    //     // console.log(this);
    //     if($(this).hasClass("active")){
    //         $(this).children(".icon-submenu").removeClass("icon-submenu lnr lnr-chevron-down").addClass("icon-submenu lnr lnr-chevron-left");
    //     }else{
    //         $(this).children(".icon-submenu").removeClass("icon-submenu lnr lnr-chevron-left").addClass("icon-submenu lnr lnr-chevron-down");
    //     }
    //
    // });
//显示遮罩层

});

function showMask(){
    $("#mask").css("height",$(document).height());
    // $("#mask").css("width",$(document).width());
    $("#mask").css("width",window.outerWidth);
    $("#mask").fadeIn(300);

}
//隐藏遮罩层
function hideMask(){
    $("#mask").fadeOut(300);
}