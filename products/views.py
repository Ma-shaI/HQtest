from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, ProductAccess
from lessons.models import Lesson, LessonViewed
from .utils import convert_to_time


class LessonsList(APIView):
    def get(self, request):
        user = request.user
        lesson_data = []
        products = Product.objects.filter(productaccess__user_profile=user)
        for product in products:
            lessons = Lesson.objects.filter(products=product.id)
            for lesson in lessons:
                dictionary = {
                    'product id': f'{product.id}',
                    'product title': product.title,
                    'lesson id': lesson.id,
                    'lesson title': lesson.title,
                    'lesson duration': convert_to_time(lesson.duration)}
                try:
                    lesson_viewed = LessonViewed.objects.filter(lesson=lesson).first()
                    lesson_viewed.mark_viewed()
                    seconds = lesson_viewed.viewing_time
                    dictionary[
                        'status'] = f'{"Просмотрено" if lesson_viewed.status else "Не просмотрено"}'
                    dictionary['viewing time'] = convert_to_time(seconds)
                    lesson_data.append(dictionary)
                except:
                    dictionary['status'] = "Не просмотрено"
                    lesson_data.append(dictionary)
        return Response(lesson_data)


class LessonList(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            lessons = Lesson.objects.filter(products=product)
            lesson_data = []
            for lesson in lessons:
                try:
                    lesson_viewed = LessonViewed.objects.filter(lesson=lesson).first()
                    lesson_viewed.mark_viewed()
                    seconds = lesson_viewed.viewing_time
                    lesson_data.append(
                        {
                            'product id': product.id,
                            'product title': product.title,
                            'lesson id': lesson.id,
                            'lesson duration': convert_to_time(lesson.duration),
                            'status': f'{"Просмотрено" if lesson_viewed.status else "Не просмотрено"}',
                            'viewing time': convert_to_time(seconds),
                            'date of last viewing': lesson_viewed.date
                        })
                except:
                    lesson_data.append({
                        'product id': product.id,
                        'product title': product.title,
                        'lesson id': lesson.id,
                        'lesson duration': convert_to_time(lesson.duration),
                        'status': "Не просмотрено"

                    })

            return Response(lesson_data)

        except:
            return Response({'error': 'Not found'}, status=404)


class LessonStatisticsList(APIView):
    def get(self, request):
        products = Product.objects.annotate(num_lessons_viewed=Count('lesson__lessonviewed'))
        statistics = []
        for product in products:
            total_viewing_time = 0
            lessons_viewed = LessonViewed.objects.filter(lesson__products=product.id)
            for lesson in lessons_viewed:
                total_viewing_time += lesson.viewing_time

            product_access_objects = ProductAccess.objects.filter(product=product.id).count()
            dictionary = {
                'product title': product.title,
                'numer_lessons_viewed': product.num_lessons_viewed,
                'product_access_objects': product_access_objects,
                'total_viewing_time': convert_to_time(total_viewing_time),
                'percentage of product purchase': f'{round((product_access_objects / User.objects.all().count()) * 100, 1)}%'
            }
            statistics.append(dictionary)

        return Response(statistics)
