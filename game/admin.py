import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Room, ChatLog

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'game_type', 'is_active', 'created_at')
    list_filter = ('game_type', 'is_active')
    search_fields = ('code',)
    readonly_fields = ('created_at',)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'room', 'sender', 'message')
    list_filter = ('room', 'sender', 'timestamp')
    search_fields = ('message', 'sender')
    readonly_fields = ('timestamp',)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"
