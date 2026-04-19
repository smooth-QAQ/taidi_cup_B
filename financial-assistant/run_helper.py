import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-u", "batch_runner.py", "--input", "附件4.xlsx", "--start", "1"],
    capture_output=True,
    text=True,
    cwd="chatbot_financial_statement"
)

print("=== STDOUT ===")
print(result.stdout)
print("=== STDERR ===")
print(result.stderr)
print(f"=== EXIT CODE: {result.returncode} ===")
