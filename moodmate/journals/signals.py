from django.db.models.signals import post_save
from django.dispatch import receiver
from journals.models import JournalEntry
from journals.search import typesense_client

@receiver(post_save, sender=JournalEntry)
def index_journal_entry(sender, instance, **kwargs):
    try:
        typesense_client.collections['journal_entries'].documents.upsert({
            'id': str(instance.id),
            'input_text': instance.input_text,
            'response_text': instance.response_text,
            'created_at': int(instance.created_at.timestamp())
        })

    except Exception as e:
        print(f"Couldn't find the collection to update: {e}")

# write a receiver for delete as well