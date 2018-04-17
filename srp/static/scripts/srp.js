$(document).ready(function () {
    /*-----------------------------------/
	/*	SIDEBAR NAVIGATION
	/*----------------------------------*/

    $('.sidebar a[data-toggle="collapse"]').on('click', function() {
        if($(this).hasClass('collapsed')) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });

    if( $('.sidebar-scroll').length > 0 ) {
        $('.sidebar-scroll').slimScroll({
            height: '95%',
            wheelStep: 2,
        });
    }

    $('.navbar-left a[data-toggle="collapse"]').on('click', function() {
        if($(this).hasClass('collapsed')) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });

    if( $('.sidebar-scroll').length > 0 ) {
        $('.sidebar-scroll').slimScroll({
            height: '95%',
            wheelStep: 2,
        });
    }



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