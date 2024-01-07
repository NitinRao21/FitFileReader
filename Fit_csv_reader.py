import csv
import sys
import subprocess
from datetime import datetime


result = subprocess.run(['python3','FitToCSV.py',sys.argv[1], ], capture_output=True, text=True)

data_field = sys.argv[2]

def highest_avg(n, value_list):
  max_n = 0
  for i in range(1, n+1):
    max_n += value_list[i]
  curr_n = max_n
  for i in range(n+1, len(value_list)):
    curr_n = curr_n - value_list[i - n+1] + value_list[i]
    max_n = max(curr_n,max_n)

  return max_n/n


def find_max(value_list):
  max_n = 0;
  for i in value_list:
    max_n = max(i, max_n)

  return max_n

def find_time(time_1, time_2):
    time_format = "%Y-%m-%d %H:%M:%S"
    datetime1 = datetime.strptime(time_1, time_format)
    datetime2 = datetime.strptime(time_2, time_format)

    difference = datetime2 - datetime1

    # Call the total_seconds() method
    seconds = difference.total_seconds()

    # Now calculate hours, minutes, and seconds
    hour = seconds // 3600
    seconds %= 3600
    minute = seconds // 60
    seconds %= 60

    formatted_output = "%02d:%02d:%02d" % (hour, minute, seconds)
    return formatted_output


csv_file = sys.argv[1][0:len(sys.argv[1]) -3] + "csv"
with open(csv_file, 'r') as fit_csv:
  reader = csv.reader(fit_csv)
  value_list = []
  time_list = []
  row_1 = next(reader)
  time_index = row_1.index("timestamp")
  try:
      if(data_field == "pace"):
        seek_value = row_1.index("distance")
      else:
        seek_value = row_1.index(data_field)
  except ValueError:
      print(f"Data field '{data_field}' not found in the CSV file.")
      subprocess.run("rm " + csv_file, shell=True)
      sys.exit(1)

  for row in reader:
    time_list.append(row[time_index])
    try:
        # Assuming pace or distance could be float values
        value = float(row[seek_value])
        value_list.append(value)
    except ValueError:
        # Handle cases where conversion to float fails
        pass

subprocess.run("rm " + csv_file, shell=True)

time = find_time(time_list[0], time_list[len(time_list) - 1])

cum_value = sum(value_list)
num_values = len(value_list)

if num_values > 0:
    avg_value = cum_value / num_values
    max_value = find_max(value_list)
else:
    avg_value = 0
    max_value = 0

#print(sec_to_time(len(value_list)))
print(time)
print("avg %s: %d\nmax %s: %d" % (data_field, avg_value, data_field, max_value))
print("best 1 min: %d\nbest %s min: %d" % (highest_avg(60, value_list), sys.argv[3], highest_avg(int(sys.argv[3]) * 60, value_list)))
