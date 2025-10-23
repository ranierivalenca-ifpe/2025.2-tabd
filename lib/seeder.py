import psycopg2

from lib._constants import DB_PASS, DB_USER
from lib import Input
import survey


class Seeder:
    def __init__(self, host, port, dbname):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=DB_USER, password=DB_PASS
        )

    def select(self, table, column, cache=True):
        cache_attr = f"_{table}_{column}_cache"
        if cache and hasattr(self, cache_attr):
            return getattr(self, cache_attr)
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {column} FROM {table}")
            res = [row[0] for row in cur.fetchall()]
            if cache:
                setattr(self, cache_attr, res)
            return res

    def seed(self, schema, rows, commit_interval=None, update_interval=100):
        with self.conn.cursor() as cur:
            # for table in rows:
            #     if table not in schema:
            #         continue
            #     inserted = 0
            #     with Input.spin(
            #         "Seeding {} rows into {}...".format(rows[table], table),
            #         "{} rows inserted into {}".format(inserted, table),
            #         func=lambda self: inserted,
            #     ):
            #         for i in range(rows[table]):
            #             values = [
            #                 self.schema[table][col]() for col in self.schema[table]
            #             ]
            #             placeholders = ", ".join(["%s"] * len(values))
            #             columns = ", ".join(self.schema[table].keys())
            #             cur.execute(
            #                 f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            #                 values,
            #             )
            #             if (i + 1) % 10 == 0:
            #                 inserted += 10
            #                 if commit_interval and (i + 1) % commit_interval < 10:
            #                     self.conn.commit()

            # for table, fields in DATA.items():
            #     num_rows = ROWS[table]
            #     field_names = ", ".join(fields.keys())
            #     for i in range(num_rows):
            #         values = ", ".join(f"'{eval(v)}'" for v in fields.values())
            #         cur.execute(f"INSERT INTO {table} ({field_names}) VALUES ({values})")
            #         if (i + 1) % 1000 == 0:
            #             print(f"{i+1} rows inserted into {table}...")

            for table in rows.keys():
                fields = schema.get(table, {})
                if table not in rows:
                    continue
                num_rows = rows[table]
                field_names = ", ".join(fields.keys())
                inserted = 0
                with Input.spin(
                    "Seeding {} rows into {}".format(num_rows, table),
                    "{} rows inserted into {}".format(num_rows, table),
                    func=lambda self: " ({} rows inserted)".format(inserted),
                    runes=(".  ", ".. ", "..."),
                ):
                    for i in range(num_rows):
                        values = [
                            fields[col]() if callable(fields[col]) else fields[col]
                            for col in fields
                        ]
                        placeholders = ", ".join(["%s"] * len(values))
                        cur.execute(
                            f"INSERT INTO {table} ({field_names}) VALUES ({placeholders})",
                            values,
                        )
                        if (i + 1) % update_interval == 0:
                            inserted += update_interval
                            if (
                                commit_interval
                                and (i + 1) % commit_interval < update_interval
                            ):
                                self.conn.commit()
            self.conn.commit()
