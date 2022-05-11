
window.addEventListener("load", function(e){
    
    //filter display toggle
    toggleFilter('orgs-section-header', 'single-filter-section.student-orgs')

    //load classes without displaing
    $('select#id_courses').children().css('display','none')

    //filters out courses by the organization selection the user makes
    //when adding a course to their profile
    $('select#id_organizations_courses').change(function(){
        var selectedOrg = $(this).children("option:selected").val()
        var optionToChange = $('select#id_courses').children(`option#${selectedOrg}`)
        optionToChange.css('display','block')
        $('select#id_courses').children(`:not(option#${selectedOrg})`).css('display','none')
    })
})