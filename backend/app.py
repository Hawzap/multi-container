import logging
import os

import psycopg2
from flask import Flask, jsonify

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "GET /health" not in record.getMessage()


logging.getLogger("werkzeug").addFilter(HealthCheckFilter())

app = Flask(__name__)
app.json.ensure_ascii = False


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users")
def get_users():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users ORDER BY id")
                rows = cursor.fetchall()
    except psycopg2.Error as error:
        app.logger.error("Помилка бази даних: %s", str(error).strip())
        return jsonify({"error": "Не вдалося отримати дані з бази даних"}), 500

    users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
    app.logger.info("Запит /users: повернено записів: %d", len(users))
    return jsonify(users)


if __name__ == "__main__":
    app.logger.info(
        "Backend запущено, база даних: %s:%s/%s",
        os.environ["DB_HOST"],
        os.environ.get("DB_PORT", "5432"),
        os.environ["DB_NAME"],
    )
    app.run(host="0.0.0.0", port=5000)
