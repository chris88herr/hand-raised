function toggleFilter(clickTargetClass, toggableSelector){
    $(`.${clickTargetClass}`).on("click", function(){
        var toggable = $(`.${toggableSelector}`)
        if(toggable.css('display') == 'none'){
            toggable.css('display', 'flex')
        }
        else {
            toggable.css('display', 'none')
        }
    })
}
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
       $('select#id_subjects').children(`option#${selectedOrg}`).css('display','block')
       $('select#id_subjects').children(`:not(option#${selectedOrg})`).css('display','none')
    })

    //toggle the orgs filter when clicking on the orgs filter header
    toggleFilter('orgs-section-header', 'single-filter-section.professor-orgs')
    toggleFilter('subjects-section-header', 'single-filter-section.professor-subjects')
    

}

