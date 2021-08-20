import datetime
from pony.orm import Database, Required, PrimaryKey, Set, Optional, db_session
from .. import config
from ..languages_enum import LanguagesEnum


db = Database(**config.bot.database)

__all__ = ["BanDetails", "User", "Group"]


class BanDetails(db.Entity):
    id = PrimaryKey(int, min=-10000000000000, size=64)
    ban_date = Required(datetime.datetime)
    ban_reason = Required(str)
    banned_by = Required("User", reverse="ban_details")


class User(db.Entity):
    id = PrimaryKey(int, min=-10000000000000, size=64)
    first_name = Required(str)
    last_name = Optional(str)
    ban_details = Optional(BanDetails, reverse="banned_by")
    banned_in_groups = Set("Group", reverse="banned_users")
    owning_groups = Set("Group", reverse="owner")
    admin_in_groups = Set("Group", reverse="administrators")


class Group(db.Entity):
    id = PrimaryKey(int, min=-10000000000000, size=64)
    owner = Optional(User, reverse="owning_groups")
    time_to_ban = Required(int, default=60)
    administrators = Set(User, reverse="admin_in_groups")
    default_language = Required(str, default=LanguagesEnum.HE)
    banned_users = Set(User, reverse="banned_in_groups")


db.generate_mapping(create_tables=True)
