# Part B - Server Log Analyzer
# Uses Counter and defaultdict to parse and summarize log data

from collections import Counter, defaultdict
import re

# ─────────────────────────────────────────────
# Simulated server log lines (format based on Python's logging module)
# Format: YYYY-MM-DD HH:MM:SS,ms LEVEL     module_name : message
# ─────────────────────────────────────────────
RAW_LOGS = [
    "2024-06-10 08:01:23,100 INFO     auth_service : User login successful for user_id=1042",
    "2024-06-10 08:01:45,200 INFO     auth_service : User login successful for user_id=1043",
    "2024-06-10 08:02:10,310 WARNING  db_service   : Slow query detected (1.8s) on table orders",
    "2024-06-10 08:02:55,410 ERROR    db_service   : Connection timeout after 3 retries",
    "2024-06-10 08:03:11,500 INFO     api_gateway  : GET /products 200 OK",
    "2024-06-10 08:03:30,600 ERROR    auth_service : Invalid token for user_id=9999",
    "2024-06-10 08:04:00,700 INFO     api_gateway  : GET /orders 200 OK",
    "2024-06-10 08:04:21,800 WARNING  auth_service : Too many failed login attempts for user_id=8888",
    "2024-06-10 08:05:05,900 ERROR    payment_svc  : Payment gateway timeout for order_id=5512",
    "2024-06-10 08:05:20,010 INFO     payment_svc  : Payment processed successfully for order_id=5500",
    "2024-06-10 08:05:45,120 ERROR    db_service   : Connection timeout after 3 retries",
    "2024-06-10 08:06:00,230 CRITICAL payment_svc  : Unhandled exception in payment flow: NullPointerError",
    "2024-06-10 08:06:15,340 ERROR    api_gateway  : 500 Internal Server Error on POST /checkout",
    "2024-06-10 08:06:40,450 WARNING  db_service   : Slow query detected (2.1s) on table orders",
    "2024-06-10 08:07:01,560 INFO     auth_service : User login successful for user_id=1044",
    "2024-06-10 08:07:22,670 ERROR    payment_svc  : Payment gateway timeout for order_id=5513",
    "2024-06-10 08:07:45,780 INFO     api_gateway  : GET /users 200 OK",
    "2024-06-10 08:08:00,890 ERROR    auth_service : Invalid token for user_id=7777",
    "2024-06-10 08:08:33,900 CRITICAL db_service   : Disk space below 5%% on /var/lib/mysql",
    "2024-06-10 08:09:00,010 INFO     api_gateway  : POST /products 201 Created",
    "2024-06-10 08:09:15,120 WARNING  payment_svc  : Retry attempt 2 for order_id=5514",
    "2024-06-10 08:09:40,230 ERROR    db_service   : Deadlock detected on table inventory",
    "2024-06-10 08:10:00,340 INFO     auth_service : User logout for user_id=1042",
    "2024-06-10 08:10:22,450 ERROR    api_gateway  : 500 Internal Server Error on POST /checkout",
    "2024-06-10 08:10:55,560 CRITICAL payment_svc  : Unhandled exception in payment flow: NullPointerError",
]

# ─────────────────────────────────────────────
# Step 1 - Parse each log line into a dict
# ─────────────────────────────────────────────
LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s+'
    r'(?P<level>\w+)\s+'
    r'(?P<module>\S+)\s*:\s+'
    r'(?P<message>.+)'
)

def parse_logs(raw_lines):
    """Parses each raw log string into a structured dict."""
    parsed = []
    for line in raw_lines:
        m = LOG_PATTERN.match(line.strip())
        if m:
            parsed.append({
                'timestamp': m.group('timestamp'),
                'level':     m.group('level'),
                'module':    m.group('module'),
                'message':   m.group('message').strip(),
            })
    return parsed


# ─────────────────────────────────────────────
# Step 2 - Counter-based analysis
# ─────────────────────────────────────────────
def analyze_with_counter(logs):
    """Uses Counter to find message freq, active modules, level distribution."""
    all_messages = [e['message'] for e in logs]
    all_modules  = [e['module']  for e in logs]
    all_levels   = [e['level']   for e in logs]

    error_messages = [e['message'] for e in logs if e['level'] == 'ERROR']

    return {
        'most_common_errors':  Counter(error_messages).most_common(3),
        'most_active_modules': Counter(all_modules).most_common(3),
        'level_distribution':  dict(Counter(all_levels)),
    }


# ─────────────────────────────────────────────
# Step 3 - Group errors by module using defaultdict(list)
# ─────────────────────────────────────────────
def errors_by_module(logs):
    """Groups ERROR-level log entries by module."""
    grouped = defaultdict(list)
    for entry in logs:
        if entry.get('level') == 'ERROR':
            grouped[entry['module']].append(entry['message'])
    return dict(grouped)


# ─────────────────────────────────────────────
# Step 4 - Summary dict
# ─────────────────────────────────────────────
def generate_summary(logs):
    """Returns a high-level summary of the log file."""
    total = len(logs)
    error_count = sum(1 for e in logs if e.get('level') == 'ERROR')
    counter_data = analyze_with_counter(logs)

    # busiest module by all log entries
    module_counts = Counter(e['module'] for e in logs)

    return {
        'total_entries':  total,
        'error_rate':     f"{round((error_count / total) * 100, 1)}%" if total else "0%",
        'top_errors':     [msg for msg, _ in counter_data['most_common_errors']],
        'busiest_module': module_counts.most_common(1)[0][0] if module_counts else None,
    }


# ─────────────────────────────────────────────
# Self-study note (as a comment, not printed)
# Python's logging module format string uses:
#   %(asctime)s %(levelname)-8s %(name)s : %(message)s
# You add it to a real app like:
#   logging.basicConfig(format='...', level=logging.DEBUG)
#   logger = logging.getLogger(__name__)
#   logger.error("something went wrong")
# ─────────────────────────────────────────────


if __name__ == '__main__':
    logs = parse_logs(RAW_LOGS)

    print("=" * 55)
    print("  SERVER LOG ANALYZER")
    print("=" * 55)

    print(f"\n[1] Total parsed entries: {len(logs)}")
    print("\n    First 3 parsed entries:")
    for entry in logs[:3]:
        print(f"    {entry}")

    counter_data = analyze_with_counter(logs)
    print("\n[2] Counter Analysis")
    print("    Most common errors:")
    for msg, cnt in counter_data['most_common_errors']:
        print(f"      ({cnt}x) {msg}")

    print("    Most active modules:")
    for mod, cnt in counter_data['most_active_modules']:
        print(f"      {mod}: {cnt} entries")

    print(f"    Level distribution: {counter_data['level_distribution']}")

    print("\n[3] Errors grouped by module:")
    for mod, msgs in errors_by_module(logs).items():
        print(f"    {mod} ({len(msgs)} errors):")
        for msg in msgs:
            print(f"      - {msg}")

    print("\n[4] Summary:")
    for k, v in generate_summary(logs).items():
        print(f"    {k}: {v}")
