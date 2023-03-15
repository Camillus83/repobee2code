# zadanie rekrutacyjne - Mikroserwis do zarządzania wydarzeniami

## Python + Django + GraphQL

Projekt X jest złożony z wielu mikroserwisów. Każdy z tych mikroserwisów komunikuje się ze
sobą za pomocą Apache Kafka. Jakakolwiek operacja w projekcie X ma być docelowo zapisana w
bazie danych mikroserwisu odpowiadającego za przechowywanie tych informacji. Należy taki
mikroserwis zaimplementować. Operacją może być np. “dodano użytkownika, zmodyfikowano
produkt, pobrano plik” itd, czyli jakakolwiek operacja zachodząca w systemie.

## Technologie

Projekt został stworzony przy użyciu nastepujacych technologii.

* Django - framework dla języka Python służący do aplikacji webowych.
* PostgreSQL - relacyjna baza danych.
* GraphQL - biblioteka graphene-relay, umożliwiająca budowę zapytań i manipulowanie w postaci strumienia danych.
* Apache Kafka - oprogramowanie służące do przesyłania danych w czasie rzeczywistym w postaci strumienia danych.
* Faust - biblioteka do przetwarzania strumieniowego w Apache Kafka.
* Docker - platforma do tworzenia i uruchamiania aplikacji w kontenerach.

## Instalacja i uruchamianie

Do uruchomienia aplikacji potrzebne są

* Docker
* Docker Compose

Aby uruchomić aplikację, należy wykonać następujące kroki:

1. Sklonowanie repozytorium z projektem,

   ```bash
   git clone git@github.com:Camillus83/repobee2code.git
   ```

2. Przejście do katalogu z projektem,

   ```bash
   cd repobee2code
   ```

3.  zmiana wartości pola `KAFKA_ADVERTISED_HOST_NAME` w docker-compose.yml aby pasował do adresu IP hosta dockera. (Nie używać localhost ani 127.0.0.1 jeśli chcesz uruchomić wielu brokerów.)

4. Uruchomienie aplikacji przy użyciu docker-compose,

   ```bash
   docker-compose up -d --build
   ```

5. Migracja bazy danych

   ```bash
   docker exec -it bee2code-task-web-1 bash
   python manage.py migrate
   ```

6. Stworzenie superusera

```bash
docker exec -it bee2code-task-web-1 bash
python manage.py createsuperuser
```

6. Wejdź na stronę `127.0.0.1:8000/graphql`, aby móc użyć GraphQL 

## Funkcjonalności

Główną funkcjonalnością mikroserwisu jest zarządzanie wydarzeniami w systemie, czyli umożliwnia dodawanie, modyfikowanie, usuwanie lub pobieranie informacji o wydarzeniach. Np.

* Dodano nowego użytkownika,.
* Dodano nowy produkt,

Dodatkowo, mikroserwis obsługuje przesyłąnie wiadomości w systemie przy wykorzystaniu Apache Kafka. Wraz z tworzeniem aplikacji tworzony jest temat o nazwie 'events'. Dzięki bibliotece faust temat jest cały czas obserwowany, i przy każdej odpowiedniej wiadomości na temat 'events' tworzony jest nowy rekord w bazie danych.

## Przykładowe zapytania

### zapytanie - Dodaj nowe wydarzenie

```json
mutation {
  createEvent(
    input: {description: "Created new user for clients.", name: "Create User", source: "users"}
  ) {
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
```

### Odpowiedź - Dodaj nowe wydarzenie

```json
{
  "data": {
    "createEvent": {
      "event": {
        "id": "RXZlbnRUeXBlOjEw",
        "name": "Create User",
        "uuid": "765fe10c-30fa-4dc0-afc5-cec823782fda",
        "createdAt": "2023-03-14T21:17:40.102215+00:00",
        "updatedAt": null,
        "description": "Created new user for clients."
      }
    }
  }
 }
```

### zapytanie - Modyfikuj wydarzenie

```json
mutation {
  updateEvent(
    input: {description: "Create new user for minion.", name: "Create User", source: "users"}
    uuid: "765fe10c-30fa-4dc0-afc5-cec823782fda"
  ) {
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
```

### Odpowiedź - Modyfikuj wydarzenie

```json
{
  "data": {
    "updateEvent": {
      "event": {
        "id": "RXZlbnRUeXBlOjEw",
        "name": "Create User",
        "uuid": "765fe10c-30fa-4dc0-afc5-cec823782fda",
        "createdAt": "2023-03-14T21:17:40.102215+00:00",
        "updatedAt": "2023-03-14T21:21:09.161382+00:00",
        "description": "Create new user for minion."
      }
    }
  }
}
```

### zapytanie - Pobierz wydarzenie o poprawnym UUID

```json
query {
  event(uuid: "765fe10c-30fa-4dc0-afc5-cec823782fda"){
    id
    name
    uuid
    createdAt
    updatedAt
    description
  }
}
```

 ### odpowiedz - Pobierz wydarzenie o poprawnym UUID

```
{
  "data": {
    "event": {
      "id": "RXZlbnRUeXBlOjIx",
      "name": "Add new product",
      "uuid": "765fe10c-30fa-4dc0-afc5-cec823782fda",
      "createdAt": "2023-03-14T21:32:49.223874+00:00",
      "updatedAt": null,
      "description": "Add new product \"Bla\" to the catalog item."
    }
  }
}
```

### zapytanie - Pobierz wydarzenie o nieistniejacym UUID

```json
query {
  event(uuid: "765fe10c-30fa-4dc0-afc5-cec823782fdb"){
    id
    name
    uuid
    createdAt
    updatedAt
    description
  }
}
```

### Odpowiedz - Pobierz wydarzenie o nieistniejącym UUID

```json
{
  "errors": [
    {
      "message": "Event with given UUID doesn't exists.",
      "locations": [
        {
          "line": 28,
          "column": 3
        }
      ],
      "path": [
        "event"
      ]
    }
  ],
  "data": {
    "event": null
  }
}
```

### zapytanie - Pobierz wydarzenia z słowem 'create' w nazwie.

```json
{
  events(name_Icontains: "create") {
    edges {
      node {
        id
        name
        uuid
        description
        source
        createdAt
        updatedAt
      }
    }
  }
}

```

### odpowiedz - Pobierz wydarzenia z słowem 'create' w nazwie.

```json
{
  "data": {
    "events": {
      "edges": [
        {
          "node": {
            "id": "RXZlbnRUeXBlOjIz",
            "name": "Create User",
            "uuid": "653cd54e-8fcd-4b31-a58e-dd84adc0ce16",
            "description": "Create new user for blal.",
            "source": "USERS",
            "createdAt": "2023-03-14T21:38:03.659180+00:00",
            "updatedAt": null
          }
        },
        {
          "node": {
            "id": "RXZlbnRUeXBlOjI0",
            "name": "Create User",
            "uuid": "6c72f37d-4b1e-43d1-a222-e0dc7524b1f9",
            "description": "Create new user for blal.",
            "source": "USERS",
            "createdAt": "2023-03-14T21:38:05.200226+00:00",
            "updatedAt": null
          }
        }
      ]
    }
  }
}
```

## Przykładowa wiadomość wysłana do Apache kafka

Aby wysłać przykładową wiadomość o wydarzeniu przy użyciu apache kafka należy:

1. Uruchomienie terminalu kontenera kafka

   ```bash
    docker exec -it bee2code-task-kafka-1 bash
   ```

2. Wysłać wiadomość na temat "events"

   ```bash
    kafka-console-producer.sh --broker-list kafka:9092 --topic events
    > {"name":"Pozdrowienia z kafki", "source":"users", "description":"Event utworzony przy 	wykorzystaniu Apache Kafka & Faust"}
    >^C
   ```

3. Sprawdzić nowe rekordy w bazie danych.

   zapytanie o rekordy:

```json
{
  events(name_Icontains: "kafki") {
    edges {
      node {
        id
        name
        uuid
        description
        source
        createdAt
        updatedAt
      }
    }
  }
}

```

odpowiedź:

```json
{
  "data": {
    "events": {
      "edges": [
        {
          "node": {
            "id": "RXZlbnRUeXBlOjI1",
            "name": "Pozdrowienia z kafki",
            "uuid": "a430d7cf-2337-41dc-8f75-da37df82444d",
            "description": "Event utworzony przy wykorzystaniu Apache Kafka & Faust",
            "source": "USERS",
            "createdAt": "2023-03-14T21:46:18.284748+00:00",
            "updatedAt": null
          }
        }
      ]
    }
  }
}
```
