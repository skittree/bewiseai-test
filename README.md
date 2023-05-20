# SQLAlchemy + FastAPI REST API Test

## Installation steps

Make sure to have [Docker](https://www.docker.com) installed and running with Compose on your local machine before setup. Use Linux containers.

1. Clone the repository to a local machine
```bash
git clone https://github.com/skittree/bewiseai-test.git
```

2. (Recommended) Edit the `.env` file in the root directory to store your own configuration parameters for the API for safety reasons.

```dotenv
QUESTION_LIMIT=500
MAX_FILESIZE_MB=100

PORT={your_api_port}
POSTGRES_USER={your_db_username}
POSTGRES_PASSWORD={your_db_password}
POSTGRES_SERVER={your_db_server}
POSTGRES_PORT={your_db_port}
POSTGRES_DB={your_db_name}
```

3. Run the script `compose.sh` to build the necessary Docker containers, images and volumes. The database tables are initialized upon launch.

## Usage

You may view the documentation and test the various API requests via Swagger UI by heading to http://server:port/docs once the API is running. 

For example, to launch on a local machine that is running the API on default port `8000`, you can use the following link: http://localhost:8000/docs.

Similarly, using the default `.env` parameters, the DB connection link is `postgresql://localhost:5432/trivia`.

Here is an example on how to connect to the database with DBeaver:

![fig1](https://github.com/skittree/bewiseai-test/assets/32728173/3f21c05e-5cda-4ae1-a8f5-d14c2f482556)
