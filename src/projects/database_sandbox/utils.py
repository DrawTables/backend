from pydbml import PyDBML


def convert_dbml_to_sql(dbml_text: str) -> str:
    parsed = PyDBML(dbml_text)
    sql = parsed.sql
    return sql
