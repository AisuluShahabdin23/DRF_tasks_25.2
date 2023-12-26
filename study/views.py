from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from study.models import Course, Lesson
from study.permissions import IsAuthor, IsManager
from study.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    """ Для вывода информации (ViewSet-класс д)"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):       # Функция привязывает автора к его курсу
        serializer.save()
        self.request.user.course_set.add(serializer.instance)

    # Если user - не модератор, то функция показывает только его курсы
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Course.objects.filter(autor=self.request.user)
        elif self.request.user.is_staff:
            return Course.objects.all()


class LessonListAPIView(ListAPIView):
    """ Отображение списка сущностей (Generic-класс)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsAuthor]


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Отображение одной сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsAuthor]


class LessonCreateAPIView(CreateAPIView):
    """ Создание сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsAuthor]

    def perform_create(self, serializer):     # Функция привязывает автора к его уроку
        new_lesson = serializer.save()
        new_lesson.author = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    """ Редактирование сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthor]


class LessonDestroyAPIView(DestroyAPIView):
    """ Удаление сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager]
