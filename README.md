# SQLAlchemy + FastAPI REST API Test

## Installation steps

Make sure to have [Docker](https://www.docker.com) available and installed on your local machine before setup.

1. Clone the repository to a local machine
```bash
git clone https://github.com/skittree/bewiseai-test.git
```

2. Create the `.env` file in the root directory from `.env.template` to store your configuration parameters for the API.

```dotenv
QUESTION_LIMIT=500
PORT=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_SERVER=
POSTGRES_PORT=
POSTGRES_DB=
```

3. Run the script `compose.sh` to build the necessary Docker containers, images and volumes. The database tables are initialized upon launch.

## Usage

### Save questions from API to database

```http
POST server:port/api/trivia?questions_num=number
```

Retrieves a `number` of random trivia questions from [jService API](https://jservice.io) and stores them in the PostgreSQL database.