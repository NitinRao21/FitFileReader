import csv
import sys
import subprocess

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

def sec_to_time(seconds):
  hour = 0
  minute = 0
  sec = 0

  sec = seconds % 60
  seconds -= sec
  seconds /= 60
  minute = seconds%60
  seconds -= minute
  seconds /= 60
  hour = seconds


  formatted_output = "%02d:%02d:%02d" % (hour, minute, sec)
  return formatted_output

csv_file = sys.argv[1][0:len(sys.argv[1]) -3] + "csv"
with open(csv_file, 'r') as fit_csv:
  reader = csv.reader(fit_csv)
  seek_value = 0
  value_list = []
  row_1 = next(reader)
  try:
      seek_value = row_1.index(data_field)
  except ValueError:
      print(f"Data field '{data_field}' not found in the CSV file.")
      subprocess.run("rm " + csv_file, shell=True)
      sys.exit(1)

  for row in reader:
    value_list.append(int(row[seek_value]))

subprocess.run("rm " + csv_file, shell=True)
cum_value = sum(value_list)

num_values = len(value_list)


print(sec_to_time(len(value_list)))
print("avg %s: %d\nmax %s: %d" % (data_field, cum_value/num_values, data_field, find_max(value_list)))
print("best 1 min: %d\nbest %s min: %d" % (highest_avg(60, value_list), sys.argv[3], highest_avg(int(sys.argv[3]) * 60, value_list)))
