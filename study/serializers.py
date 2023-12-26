from rest_framework import serializers
from study.models import Lesson, Course


class LessonCourseSerializer(serializers.ModelSerializer):
    """ Cериализатор для Course, который будет включать данные об уроках """
    class Meta:
        model = Lesson
        fields = ('pk', 'title_course',)


class CourseCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания Course"""
    class Meta:
        model = Course
        fields = ('title_course', 'description_course',)


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Course"""
    lessons_count = serializers.SerializerMethodField()  # поле вывода количества уроков
    lessons = LessonCourseSerializer(source='lesson_set', read_only=True, many=True)  # поле вывода уроков

    def get_lessons_count(self, instance):
        """ Метод вывода количества уроков """
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = ('pk', 'title_course', 'image_course', 'description_course', 'lessons_count', 'lessons')


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Lesson """
    class Meta:
        model = Lesson
        fields = '__all__'  # Вывод всех полей
