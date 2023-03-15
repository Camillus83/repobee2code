"""
Representation of Kafka consumer that listen to the messages,
and creates events from message data via GraphQL.
"""
from faust import App, Record
import requests


class KafkaMessage(Record):
    """
    Representation of a message received from a Kafka topic.
    """

    source: str
    name: str
    description: str


app = App(
    "eventcatcher", broker="kafka://kafka:9092"
)  
topic = app.topic(
    "events", value_type=KafkaMessage
)  


@app.agent(topic)
async def process_messages(messages):
    """
    Process message from Kafka topic, create Event record via a GraphQL API and print response.
    """
    url = "http://web:8000/graphql"
    session = requests.Session()
    # response = session.get(url)
    # csrftoken = response.cookies.get("csrftoken")
    headers = {
        "Content-Type": "application/json",
        #"X-CSRFToken": csrftoken,
    }
    async for message in messages:
        mutation = """
        mutation CreateEvent($name: String!, $description: String!, $source: String!) {
            createEvent(input: {name: $name, description: $description, source: $source}) {
                event {
                    id
                    name
                    uuid
                    createdAt
                    updatedAt
                    description
                    }
                }
            }
"""
        variables = {
            "name": message.name,
            "description": message.description,
            "source": message.source,
        }

        response = requests.post(
            url, json={"query": mutation, "variables": variables}, headers=headers
        )
        print(response)


app.main()
