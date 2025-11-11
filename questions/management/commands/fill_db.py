import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import UserProfile
from questions.models import Question, QuestionAnswer, Tag, QuestionLike, AnswerLike


from faker import Faker
class Command(BaseCommand):
    help = "Заполнение БД"

    def add_arguments(self, parser):
        parser.add_argument('--count', type = int)


    def handle(self, *args, **options):
        count = options.get('count')
        fake = Faker('ru_RU')

        num_users = count
        num_tags = count 
        num_questions = count * 10
        num_answers = count * 10
        # num_marks = count * 200

        users = []
        for i in range (num_users):
            userb, _ = User.objects.update_or_create(
                username = f"user {i}",
                email = fake.email(),
                is_staff = False,
                is_superuser = False,
                password = "123456"
            )
            userProf,_ = UserProfile.objects.update_or_create(
                user = userb,
                nickname = fake.user_name(),
                avatar = None
            )
            users.append(userProf)
        
        print("Users created")

        tags, seen_tags = [], set()

        while len(tags) < num_tags:
            tagname = fake.pystr(4,20)
            if tagname in seen_tags:
                continue
            tag, created = Tag.objects.get_or_create(title = tagname)
            if created:
                tags.append(tag)
                seen_tags.add(tagname)
        
        print("Tags created")

        questions = []
        for i in range(num_questions):
            question = Question.objects.create(
                title=fake.sentence()[:60],
                question_text=fake.text(max_nb_chars=500),
                author=random.choice(users),
                is_hot=fake.boolean(chance_of_getting_true=20),
                like_count = 0,
                answer_count = 0
            )
            
            question_tags = random.sample(tags, random.randint(3, 6))
            question.tags.set(question_tags)

            questions.append(question)

        print("Questions created")

        answers = []
        temp_count = 0
        while temp_count < num_answers:
            for _ in range(random.randint(3, 20)):
                temp_count += 1
                answer = QuestionAnswer.objects.create(
                    author=random.choice(users),
                    text=fake.text(max_nb_chars=300),
                    question=question,
                    is_correct=fake.boolean(chance_of_getting_true=10),
                    like_count = 0
                )
                answers.append(answer)

        print("Answers created")

        for question in questions:
            likers = random.sample(users, random.randint(0, min(10, len(users))))
            for liker in likers:
                try:
                    QuestionLike.objects.create(
                        question=question,
                        author=liker,
                        status=fake.boolean(chance_of_getting_true=80)
                    )
                except:
                    pass 
        print("Question likes created")

        for answer in answers:
            likers = random.sample(users, random.randint(0, min(8, len(users))))
            for liker in likers:
                try:
                    AnswerLike.objects.create(
                        answer=answer,
                        author=liker,
                        status=fake.boolean(chance_of_getting_true=80)
                    )
                except:
                    pass
        print("Answer likes created")





        

