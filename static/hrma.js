window.onload = (e)=>{
    $('.close-span').on("click", function(){
        $(this).parent().parent().css('display', 'none')
    })
    $('.add-form-btn').on('click', function(){
        console.log($(this).parent().parent(), 'clicked')
        $(this).parent().parent().find('.add-form').css('display','flex')
    })

    //filters out subjects by the organization selection the user makes
    //when adding a subject to their profile
    $('select#id_organizations_subjects').change(function(){
        var selectedOrg = $(this).children("option:selected").val()
        subjects=$('select#id_subjects').children(`option#${selectedOrg}`)
        console.log(subjects)
        subjects.css('display','block')
    })

}

