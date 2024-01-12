#Written by wai.phyo6
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

sender = 'notify2@frontiir.net'
recipient = 'myo.m.htun@frontiir.net'
cc = 'sysops@frontiir.net'

def send_mail(html_content):
    try:
        SMTP_SERVER = 'zcs.frontiir.net'
        SMTP_PORT = 587
        session = smtplib.SMTP('zcs.frontiir.net', 587)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(sender, 'sdfljlERsdf34#')

        msg = MIMEMultipart()
        msg['From'] = 'Notify <notify2@frontiir.net>'
        msg['To'] = recipient
        msg['Cc'] = cc
        msg['Subject'] = '[Alert] Object Storage Size Check'

        # Add the HTML content to the email body
        msg.attach(MIMEText(html_content, 'html'))

        session.send_message(msg)
        session.quit()
        print("Mail Sent Successfully")
    except Exception as e:
        print(f"Error: unable to send - {str(e)}")

def create_html_table(content, current_date):
    table_start = "<table border='1' style='border-collapse: collapse; font-size: 14px;'>"
    table_end = "</table>"
    headers = "<tr><th style='width: 200px; height: 30px; background-color:DodgerBlue;'>Bucket</th><th style='width: 200px; background-color:DodgerBlue;'>Size</th></tr>"
    rows = ""
    bucket_data = []  # List to hold bucket data for sorting
    total_size = 0

    # Parse content to collect bucket data for sorting
    for line in content.split('\n'):
        line = line.strip()
        if line:  # Ignore empty lines
            parts = line.split(': ')
            if len(parts) == 2:
                bucket, size = parts

                # Calculate size in bytes for sorting
                size_value = float(size[:-1])
                size_unit = size[-1]
                size_in_bytes = size_value * (1024 if size_unit == 'T' else 1)

                # Append bucket data for sorting
                bucket_data.append((bucket, size, size_in_bytes))
                total_size += size_value * (1024 if size_unit == 'T' else 1)

            else:
                print(f"Invalid data format: {line}")

    # Sort bucket data based on size
    sorted_buckets = sorted(bucket_data, key=lambda x: x[2], reverse=True)

    # Generate HTML table rows from sorted data
    for bucket_info in sorted_buckets:
        bucket, size, _ = bucket_info

        # Check if size exceeds 10T to apply conditional styling
        size_value = float(size[:-1])
        size_unit = size[-1]
        size_in_bytes = size_value * (1024 if size_unit == 'T' else 1)
        row_style = "background-color: red;" if size_in_bytes >= 10 * 1024 else ""

        rows += f"<tr style='{row_style}'><td style='width: 200px; height: 20px;'>{bucket}</td><td style='width: 200px;'>{size}</td></tr>"

    # Convert the total size back to the appropriate unit (T, G, etc.)
    total_size /= 1024  # Convert total size back to the original unit
    total_unit = 'T' if total_size >= 1 else 'G'
    total_size = f"{total_size:.1f}{total_unit}"

    # Include the total size row in the table
    total_row_style = "background-color: red;" if total_size[:-1] == 'T' and float(total_size[:-1]) >= 10 else ""
    total_row = f"<tr style='{total_row_style}'><td style='height: 20px;'>Total Size</td><td>{total_size}</td></tr>"

    # Include the current date in the email body
    date_message = f"<p>Report Date: {current_date}</p>"

    html_content = f"<html><body>{date_message}{table_start}{headers}{rows}{total_row}{table_end}</body></html>"
    return html_content

if __name__ == '__main__':
    path_to_file = 'result.txt'
    path = Path(path_to_file)

    current_date = datetime.now().strftime("%a %b %d %H:%M:%S %z %Y")

    if path.is_file():
        with open(path_to_file, 'r') as file:
            content = file.read()

        html_table = create_html_table(content, current_date)

        if html_table:
            send_mail(html_table)
    else:
        print("Result file not found.")

