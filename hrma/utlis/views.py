
from hrma.models import Organization, Professor,Subject, Course

def processProfessorPOSTRequests(request):
    professor = Professor.objects.filter(pk=request.user).first()
    if 'add_org_form' in request.POST:
        org = Organization.objects.filter(pk=request.POST['organizations']).first()
        print(f'Adding Org  {org}  to Professor to {professor}')
        professor.organizations.add(org)
    elif 'add_subject_form' in request.POST:
        subjectId = request.POST['subject']
        subject = Subject.objects.filter(pk=subjectId)
        print(f'adding subject {subject} to professor {professor.user.username}')
        professor.subjects.add(subjectId)
    elif 'add_course_form' in request.POST:
        courseName = request.POST['course']
        subject = Subject.objects.filter(id=request.POST['subject']).first()
        Course.objects.create(
            course_name=courseName,
            subject=subject,
            professor=professor
            )
        