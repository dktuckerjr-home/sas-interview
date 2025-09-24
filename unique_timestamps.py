# This program creates a timestamps file used to test the unique timestamp program.

import argparse
import re
from datetime import datetime, timezone

def write_unique_dates(output_file, unique_dates):
    with open(output_file, "w", newline="") as outfile:
        for adate in sorted(unique_dates.keys()):
            outfile.write(f"{adate}\n")

def unique_date_strings(args, date_regex):
    """
    Treat the entries in the input file as strings.
    Verify that each line conforms to the expected ISO8601 format.
    """
    unique_dates = {}

    with open(args.in_file, "r") as infile:
        for adate in infile:
            adate = adate.strip()
            if date_regex.fullmatch(adate) is not None:
                unique_dates[adate] = 1

    write_unique_dates(args.out_file, unique_dates)

def unique_datetimes(args, date_regex):
    """
    Treat the entries in the input file as datetimes.
    Verify that each line conforms to the expected ISO8601 format.
    Timestamps ending with 'Z' are changed to '+00:00" since
       datetime.fromisoformat() does not recognize 'Z' as a valid timezone.
    Convert the resulting datetime to UTC for comparison purpuses.
    This means that any time that is the same but with different timezones will
       be interpreted as the same datetime.
    """
    unique_dates = {}

    with open(args.in_file, "r") as infile:
        for adate in infile:
            adate = adate.strip()
            if date_regex.fullmatch(adate) is not None:
                if adate[-1] == "Z":
                    adate = adate[:-1] + "+00:00"

                try:
                    adate_dt = datetime.fromisoformat(adate)
                except ValueError:
                    pass
                else:
                    adate_z = adate_dt.astimezone(tz=timezone.utc)
                    adate_str = adate_z.strftime("%Y-%m-%dT%H:%M:%SZ")
                    unique_dates[adate_str] = 1


    write_unique_dates(args.out_file, unique_dates)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find unique timestamps")
    parser.add_argument("in_file", help="Contains timestamps")
    parser.add_argument("out_file", help="Output file, contains unique timestammps")
    parser.add_argument("-handler", help="Use string or datetime comparison",
        choices=["string", "datetime"], default="string")

    args = parser.parse_args()

    date_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})"
    date_regex = re.compile(date_pattern)
    if args.handler == "string":
        unique_date_strings(args, date_regex)
    elif args.handler == "datetime":
        unique_datetimes(args, date_regex)
