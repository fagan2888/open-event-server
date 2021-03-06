from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from app.api.helpers.utilities import dasherize
from app.models.session import Session
from app.models.speaker import Speaker
from app.models.sponsor import Sponsor


class EventStatisticsGeneralSchema(Schema):
    """
    Api schema for general statistics of event
    """

    class Meta:
        """
        Meta class
        """

        type_ = 'event-statistics-general'
        self_view = 'v1.event_statistics_general_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

    id = fields.Str()
    identifier = fields.Str()
    sessions_draft = fields.Method("sessions_draft_count")
    sessions_submitted = fields.Method("sessions_submitted_count")
    sessions_accepted = fields.Method("sessions_accepted_count")
    sessions_confirmed = fields.Method("sessions_confirmed_count")
    sessions_pending = fields.Method("sessions_pending_count")
    sessions_rejected = fields.Method("sessions_rejected_count")
    sessions_withdrawn = fields.Method("sessions_withdrawn_count")
    sessions_canceled = fields.Method("sessions_canceled_count")
    speakers = fields.Method("speakers_count")
    sessions = fields.Method("sessions_count")
    sponsors = fields.Method("sponsors_count")

    def sessions_draft_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='draft', deleted_at=None
        ).count()

    def sessions_submitted_count(self, obj):
        return Session.query.filter_by(event_id=obj.id, deleted_at=None).count()

    def sessions_accepted_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='accepted', deleted_at=None
        ).count()

    def sessions_confirmed_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='confirmed', deleted_at=None
        ).count()

    def sessions_pending_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='pending', deleted_at=None
        ).count()

    def sessions_rejected_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='rejected', deleted_at=None
        ).count()

    def sessions_withdrawn_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='withdrawn', deleted_at=None
        ).count()

    def sessions_canceled_count(self, obj):
        return Session.query.filter_by(
            event_id=obj.id, state='canceled', deleted_at=None
        ).count()

    def speakers_count_type(self, obj, state='pending'):
        return (
            Speaker.query.join(Speaker.sessions)
            .distinct(Speaker.id)
            .filter(
                Speaker.event_id == obj.id,
                Speaker.deleted_at == None,
                Session.state == state,
            )
            .count()
        )

    def speakers_count(self, obj):
        accepted = self.speakers_count_type(obj=obj, state='accepted')
        confirmed = self.speakers_count_type(obj=obj, state='confirmed')
        pending = self.speakers_count_type(obj=obj, state='pending')
        rejected = self.speakers_count_type(obj=obj, state='rejected')
        withdrawn = self.speakers_count_type(obj=obj, state='withdrawn')
        canceled = self.speakers_count_type(obj=obj, state='canceled')
        total = Speaker.query.filter_by(event_id=obj.id, deleted_at=None).count()
        serial_data = {
            'accepted': accepted,
            'confirmed': confirmed,
            'pending': pending,
            'rejected': rejected,
            'withdrawn': withdrawn,
            'canceled': canceled,
            'total': total,
        }
        return serial_data

    def sessions_count(self, obj):
        return Session.query.filter_by(event_id=obj.id, deleted_at=None).count()

    def sponsors_count(self, obj):
        return Sponsor.query.filter_by(event_id=obj.id, deleted_at=None).count()
