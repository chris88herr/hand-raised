from hrma.models import Subject

def getSubjectsQuerySetListFromOrg(orgs):
    subjectQuerySetList = []
    for org in orgs:
                orgSubjects = Subject.objects.filter(organization=org)
                subjectQuerySetList.append(orgSubjects)

    return subjectQuerySetList