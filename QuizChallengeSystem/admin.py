from django.contrib import admin
from .models import Quiz, Question, Choice, QuizResult, UserAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answer', 'is_correct']


class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'quiz', 'formatted_score', 'created_at']
    list_filter = ['created_at', 'user', 'quiz']
    search_fields = ['user__username', 'quiz__name']
    inlines = [UserAnswerInline]
    readonly_fields = ['session_id', 'formatted_score', 'created_at']

    def formatted_score(self, obj):
        return f"{obj.score} / {obj.total_questions}"

    formatted_score.short_description = 'Score'


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
