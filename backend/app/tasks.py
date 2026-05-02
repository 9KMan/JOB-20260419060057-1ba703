import os
from celery import Celery

celery = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

celery.conf.update(task_serializer='json', accept_content=['json'],
                   result_serializer='json', timezone='UTC', enable_utc=True)

@celery.task
def send_booking_confirmation(booking_id):
    from app import create_app, db
    from app.models import Booking
    app = create_app()
    with app.app_context():
        booking = Booking.query.get(booking_id)
        if booking:
            print(f"Booking confirmation sent for booking {booking_id}")
            return True
        return False

@celery.task
def parse_artist_bio_with_ai(bio_text):
    from app import create_app
    app = create_app()
    with app.app_context():
        openai_key = app.config.get('OPENAI_API_KEY')
        if not openai_key:
            return {'error': 'OpenAI not configured'}
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract key information from this artist bio."},
                    {"role": "user", "content": bio_text}
                ]
            )
            return {'result': response.choices[0].message.content}
        except Exception as e:
            return {'error': str(e)}

@celery.task
def generate_booking_summary(booking_id):
    from app import create_app, db
    from app.models import Booking, Artist, Venue
    app = create_app()
    with app.app_context():
        booking = Booking.query.get(booking_id)
        if not booking:
            return {'error': 'Booking not found'}
        artist = Artist.query.get(booking.artist_id)
        venue = Venue.query.get(booking.venue_id)
        summary = f"Booking: {booking.event_name}, Date: {booking.event_date}, Artist: {artist.name if artist else 'Unknown'}, Venue: {venue.name if venue else 'Unknown'}, Total: ${booking.total_price}"
        return {'summary': summary}
