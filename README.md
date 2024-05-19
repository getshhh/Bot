# Awesome Telegram Bot with Dockerized PostgreSQL Database

Welcome to the README for our awesome Telegram bot, built using the aiogram library for interacting with the Telegram API, and leveraging a PostgreSQL database containerized with Docker.

## Functionality

1. **Admin Rights Assignment:**
   - Upon an administrator's command, the bot can assign administrative privileges to other users.

2. **Assignment of Homework:**
   - The bot can assign homework tasks upon user request.

3. **Balance Issuance with One-Time Code:**
   - Users can receive coins by sending a one-time code issued by an administrator.

4. **Balance View:**
   - Users can view their balance by clicking on the 'balance' button.

## Installation and Usage

1. **Install Dependencies:**
pip install aiogram
pip install psycopg2-binary
pip install SQLAlchemy

2. **Set Up PostgreSQL Database with Docker:**
- Install Docker on your system.
- Pull the PostgreSQL Docker image: `docker pull postgres`
- Run a PostgreSQL container: `docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres`

3. **Run the Bot:**
- Execute the `bot.py` file:
  ```
  python bot.py
  ```

## Bot Configuration

1. **Telegram Token:**
- Obtain a token for your bot by contacting [@BotFather](https://t.me/BotFather).
- Insert the obtained token into the corresponding place in your bot's code.

2. **Database Configuration:**
- Specify the connection parameters to your PostgreSQL database in the bot's code.

3. **Admin Rights Configuration:**
- Define the command that will assign administrative rights and specify any necessary parameters in the bot's code.

## Contributors

- [Nikita] - DevOps
- [Denis] - programmer

