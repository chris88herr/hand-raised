
from hrma.models import *


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
        
def processStudentPOSTRequest(request):
    student = Student.objects.filter(pk=request.user).first()
    if 'add_course_form' in request.POST:
        course = Course.objects.filter(pk=request.POST['courseId']).first()
        print(f'Adding COURSE  {course}  to Student to {student}')
        student.course_set.add(course)
        print(student.course_set)

    elif 'create_question_form' in request.POST:
        question_title = request.POST['question_title']
        question_text = request.POST['question_text']
        question_subject_name = request.POST['question_subject_name']
        subject_org_id =  request.POST['subject_org_id']
        
        subject =  Subject.objects.filter(name__startswith=question_subject_name, organization=subject_org_id).first()
        print(f'creating question..')
        Question.objects.create(
            author_by = student,
            question_title =question_title,
            question_text = question_text,
            question_subject= subject
        )
        print(f'added qeustion {question_title} to student {student.user.username}')

    elif 'post_answer_form' in request.POST:
        answer_text = request.POST['answer_text']
        answer_question_id = request.POST['answer_question_id']
        answer_approval_professor_id = request.POST['answer_approval_professor_id']
        print(f'posting answer from {student}')
        answer = Answer.objects.create(
            answer_text=answer_text,
            author_by=student,
            approval_professor = Professor.objects.filter(pk=answer_approval_professor_id),
            question = Question.objects.filter(pk=answer_question_id)
            )
        print(f'success: { answer}')
    elif 'add_question_commnent_form':
        print(f'posting question_comment from {student}')
        comment_text = request.POST['comment_text']
        question_id =  request.POST['question_id']
        question_comment = QuestionComment.objects.create(
            comment_text=comment_text,
            question = Question.objects.filter(pk=question_id),
            author = student
        )
        print(f'success: {question_comment}')
    elif 'add_answer_comment_form':
        print(f'posting question_comment from {student}')

        comment_text = request.POST['comment_text']
        answer_id = request.POST['answer_id']
        answer_comment = AnswerComment.objects.create(
            comment_text = comment_text,
            answer = Answer.objects.filter(pk=answer_id),
            author = student
        )

        print(f'success: {answer_comment}')
        pass