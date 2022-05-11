ACTIVE_FILTER_CLASS = 'active-filter'

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
function containsCLass(element, className){
    result = false
    classList = element.attr('class').split(' ')
    classList.forEach(function(singleClass){
        if (singleClass==className){
            console.log('found class')
            result = true
        }
    })
    return result
}
function toggleCourseFilter(element,filterClass){
    if(!containsCLass(element, filterClass )){
        element.addClass(filterClass)
        return true
    }
    else{
        element.removeClass(filterClass)
        return false
    }
}

function checkForSubstrings(string, substrings){
    result = false;
    substrings.forEach(function(substring){
        if(string.includes(substring)){
            result = true
        }
    })
    return result
}
function filterCoursesList(coursesList){
    filters = []
     $('.single-filter-section').children().each(function(){
         if(containsCLass($(this), ACTIVE_FILTER_CLASS)){
             filters.push($(this).attr('id'))
         }
     })
     console.log(filters)
     if(filters.length==0){ //no filters, show everything
        coursesList.each(function(){
                $(this).css('display', 'block')
        })
     }else{
        
        coursesList.each(function(){
            singleCourseId = $(this).attr('id')
            console.log(singleCourseId, filters, checkForSubstrings(singleCourseId,filters))
            if(checkForSubstrings(singleCourseId,filters)){
                $(this).css('display', 'block')
            }
            else{
                $(this).css('display', 'none')

            }
        })
    }
}
function filterCoursesEventListeners(){
    $('.single-filter-section').children().each(function(){
        // console.log($(this).attr('class'))
        $(this).on('click',function(){
            
            filterId = $(this).attr('id')
            coursesList = $('.user-courses-list').children()
            activated = toggleCourseFilter($(this), ACTIVE_FILTER_CLASS)
            filterCoursesList(coursesList)
            
        })
    })
}
window.addEventListener("load", (e)=>{
    $('.close-span').on("click", function(){
        $(this).parent().parent().css('display', 'none')
    })
    $('.add-form-btn').on('click', function(){
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
    
    filterCoursesEventListeners()

}
)
