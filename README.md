# SQLAlchemy + FastAPI REST API Test

## Installation steps

Make sure to have [Docker](https://www.docker.com) installed and running on your local machine before setup.

1. Clone the repository to a local machine
```bash
git clone https://github.com/skittree/bewiseai-test.git
```

1. Create the `.env` file in the root directory from `.env.template` to store your configuration parameters for the API.

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

You view the documentation and test the various API requests via Swagger UI by heading to `http://server:port/docs` once the API is running.