from datetime import datetime
from decimal import Decimal

import pytz
from flask import jsonify
from flask_login import current_user
from flask_restful import Resource, reqparse

from controllers.console import api
from controllers.console.app.wraps import get_app_model
from controllers.console.wraps import account_initialization_required, setup_required
from extensions.ext_database import db
from libs.helper import DatetimeString
from libs.login import login_required
from models.model import AppMode


def date_convert(field: str = "created_at") -> str:
    """##MySQL/Oracle
    根据不同的数据库方言（MySQL、PostgreSQL或Oracle），生成将指定时间字段从UTC时区转换为目标时区并截取日期部分的SQL查询语句。

    参数:
        field (str): 要转换的时间字段名，默认值为"created_at"。

    返回:
        str: 生成的SQL查询语句。
    """
    # 获取数据库引擎的方言名称，用于判断当前使用的是哪种数据库
    dialect = db.engine.dialect.name

    # 根据不同的数据库方言，设置不同的时间转换表达式
    if dialect == "mysql":
        # 对于MySQL数据库，使用CONVERT_TZ函数将时间从UTC时区转换为目标时区（:tz表示时区参数）
        date_convert = f"CONVERT_TZ({field}, 'UTC', :tz)"
    elif dialect == "postgresql":
        # 对于PostgreSQL数据库，使用AT TIME ZONE将时间从UTC时区转换为目标时区，并使用DATE_TRUNC函数截取到天
        date_convert = f"DATE_TRUNC('day', {field} AT TIME ZONE 'UTC' AT TIME ZONE :tz )"
    elif dialect == "oracle":
        # 对于Oracle数据库，使用FROM_TZ和AT TIME ZONE将时间从UTC时区转换为目标时区，并使用TRUNC函数截取到天
        date_convert = f"TRUNC(FROM_TZ(CAST({field} AS TIMESTAMP), 'UTC') AT TIME ZONE :tz)"

    # 拼接SQL查询语句，使用DATE函数将转换后的时间截取为日期类型，并命名为date
    sql_query = f"""SELECT
    DATE({date_convert}) AS date,"""

    # 返回生成的SQL查询语句
    return sql_query

class DailyMessageStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert()
            + """
    COUNT(*) AS message_count
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "message_count": i.message_count})

        return jsonify({"data": response_data})


class DailyConversationStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert()
            + """
    COUNT(DISTINCT messages.conversation_id) AS conversation_count
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "conversation_count": i.conversation_count})

        return jsonify({"data": response_data})


class DailyTerminalsStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert()
            + """
    COUNT(DISTINCT messages.from_end_user_id) AS terminal_count
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "terminal_count": i.terminal_count})

        return jsonify({"data": response_data})


class DailyTokenCostStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (##Oracle
            date_convert()
            + """
    (SUM(messages.message_tokens) + SUM(messages.answer_tokens)) AS token_count,
    SUM(total_price) AS total_price
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {"date": str(i.date), "token_count": i.token_count, "total_price": i.total_price, "currency": "USD"}
                )

        return jsonify({"data": response_data})


class AverageSessionInteractionStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model(mode=[AppMode.CHAT, AppMode.AGENT_CHAT, AppMode.ADVANCED_CHAT])
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert("c.created_at")
            + """
    AVG(subquery.message_count) AS interactions
FROM
    (
        SELECT
            m.conversation_id,
            COUNT(m.id) AS message_count
        FROM
            conversations c
        JOIN
            messages m
            ON c.id = m.conversation_id
        WHERE
            c.override_model_configs IS NULL
            AND c.app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND c.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND c.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += """
        GROUP BY m.conversation_id
    ) subquery
LEFT JOIN
    conversations c
    ON c.id = subquery.conversation_id
GROUP BY
    date
ORDER BY
    date"""

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {"date": str(i.date), "interactions": float(i.interactions.quantize(Decimal("0.01")))}
                )

        return jsonify({"data": response_data})


class UserSatisfactionRateStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert("m.created_at")
            + """
    COUNT(m.id) AS message_count,
    COUNT(mf.id) AS feedback_count
FROM
    messages m
LEFT JOIN
    message_feedbacks mf
    ON mf.message_id=m.id AND mf.rating='like'
WHERE
    m.app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {
                        "date": str(i.date),
                        "rate": round((i.feedback_count * 1000 / i.message_count) if i.message_count > 0 else 0, 2),
                    }
                )

        return jsonify({"data": response_data})


class AverageResponseTimeStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model(mode=AppMode.COMPLETION)
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert()
            + """
    AVG(provider_response_latency) AS latency
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "latency": round(i.latency * 1000, 4)})

        return jsonify({"data": response_data})


class TokensPerSecondStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = (
            date_convert()
            + """
    CASE
        WHEN SUM(provider_response_latency) = 0 THEN 0
        ELSE (SUM(answer_tokens) / SUM(provider_response_latency))
    END as tokens_per_second
FROM
    messages
WHERE
    app_id = :app_id"""
        )
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "tps": round(i.tokens_per_second, 4)})

        return jsonify({"data": response_data})


api.add_resource(DailyMessageStatistic, "/apps/<uuid:app_id>/statistics/daily-messages")
api.add_resource(DailyConversationStatistic, "/apps/<uuid:app_id>/statistics/daily-conversations")
api.add_resource(DailyTerminalsStatistic, "/apps/<uuid:app_id>/statistics/daily-end-users")
api.add_resource(DailyTokenCostStatistic, "/apps/<uuid:app_id>/statistics/token-costs")
api.add_resource(AverageSessionInteractionStatistic, "/apps/<uuid:app_id>/statistics/average-session-interactions")
api.add_resource(UserSatisfactionRateStatistic, "/apps/<uuid:app_id>/statistics/user-satisfaction-rate")
api.add_resource(AverageResponseTimeStatistic, "/apps/<uuid:app_id>/statistics/average-response-time")
api.add_resource(TokensPerSecondStatistic, "/apps/<uuid:app_id>/statistics/tokens-per-second")
