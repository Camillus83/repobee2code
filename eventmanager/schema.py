import graphene
from graphene_django import DjangoObjectType
from .models import Event
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "description": ["exact", "icontains", "istartswith"],
            "source": ["exact", "icontains"],
            "created_at": ["exact", "gte", "lte"],
            "updated_at": ["exact", "gte", "lte"],
        }
        fields = (
            "id",
            "name",
            "uuid",
            "source",
            "created_at",
            "updated_at",
            "description",
        )
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)
    events = DjangoFilterConnectionField(EventType)
    event = graphene.Field(EventType, uuid=graphene.UUID(required=True))

    def resolve_events(root, info, **kwargs):
        try:
            return Event.objects.all()
        except Event.DoesNotExist:
            return GraphQLError("No events found.")

    def resolve_event(root, info, uuid, **kwargs):
        try:
            return Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            return GraphQLError("Event with given UUID doesn't exists.")

    def resolve_all_events(root, info, **kwargs):
        try:
            return Event.objects.all()
        except Event.DoesNotExist:
            return GraphQLError("No events found.")


class EventInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    source = graphene.String(required=True)


class CreateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        input = EventInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        event = Event.objects.create(
            name=input.name, description=input.description, source=input.source
        )
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        input = EventInput(required=True)
        uuid = graphene.UUID()

    @classmethod
    def mutate(cls, root, info, input, uuid):
        try:
            event = Event.objects.get(uuid=uuid)
            event.name = input.name
            event.description = input.description
            event.source = input.source
            event.save()
            return UpdateEvent(event=event)
        except Event.DoesNotExist:
            return GraphQLError("Event with given UUID does not exists.")


class DeleteEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, uuid):
        try:
            event = Event.objects.get(uuid=uuid)
            event.delete()
        except Event.DoesNotExist:
            return GraphQLError("Event with given UUID does not exists.")


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
