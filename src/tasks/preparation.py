from datetime import datetime, timedelta
import pandas as pd

def get_tomorrow_weekday_abbr() -> str:
    next_day = datetime.now() + timedelta(days=1)
    return ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][next_day.weekday()]

def get_active_courses_by_weekday(course_table:pd.DataFrame, weekday_ger_abb:str) -> list[dict]:
    return course_table[
      (course_table['is_registration_active']) &
      (course_table['weekday_ger_abb'] == weekday_ger_abb)
      ].to_dict(orient="records")

