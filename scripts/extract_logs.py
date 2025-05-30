# scripts/extract_logs.py

input_path = "logs/sample.log"
output_path = "docs/generated/log_summary.md"

with open(input_path, "r") as infile:
    lines = infile.readlines()

errors = [line for line in lines if "ERROR" in line or "WARN" in line]

with open(output_path, "w") as outfile:
    outfile.write("# Log Summary\n\n")
    if not errors:
        outfile.write("No ERROR or WARN lines found.\n")
    else:
        for line in errors:
            outfile.write(f"- {line}")
