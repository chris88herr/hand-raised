window.onload = (e)=>{
    $('.close-span').on("click", function(){
        $(this).parent().parent().css('display', 'none')
    })
    $('.add-form-btn').on('click', function(){
        console.log($(this).parent().parent(), 'clicked')
        $(this).parent().parent().find('.add-form').css('display','flex')
    })

}

