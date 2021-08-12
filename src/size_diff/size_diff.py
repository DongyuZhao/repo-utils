import csv
import glob
import os

size_columns = ['Size', 'Path']
diff_columns = ['Initial', 'Final', 'Delta', 'Path']

baseline_path = '/Volumes/Builds/size_measure/baseline/ipa'
change_path = '/Volumes/Builds/size_measure/change/ipa'

output_path = '/Volumes/Builds/size_measure/reports/'
suffix = 'ipa'

def list_of_files(dir):
    return filter(os.path.isfile, glob.glob(dir + '/**/*', recursive=True))

def files_with_size(dir):
    return { str(file_path).removeprefix(dir + '/'): os.stat(file_path).st_size for file_path in list_of_files(dir) }

def write_report(dir, header, content):
    with open(dir, "w") as f:
        writer = csv.DictWriter(f, fieldnames = header)
        writer.writeheader()
        for row in content:
            writer.writerow(row)

def convert_file_dict_to_list(dict):
    result = []
    for path in dict:
        result.append({ 'Size': dict[path], 'Path': path })
    return result

def calculate_diff(baseline, change):
    result = []
    merged_list = set(baseline.keys()).union(set(change.keys()))
    for path in merged_list:
        if path in baseline.keys():
            if path in change.keys():
                delta = change[path] - baseline[path]
                if delta != 0:
                    result.append({ 'Initial': baseline[path], 'Final': change[path], 'Delta': delta, 'Path': path })
            else:
                result.append({ 'Initial': baseline[path], 'Final': 0, 'Delta': -baseline[path], 'Path': path })
        else:
            result.append({ 'Initial': 0, 'Final': change[path], 'Delta': change[path], 'Path': path })
    return sorted(result, key=lambda k: k['Delta'], reverse = True)

baseline = files_with_size(baseline_path)
change = files_with_size(change_path)
diff = calculate_diff(baseline, change)

write_report(output_path + 'baseline_' + suffix + '.csv', size_columns, convert_file_dict_to_list(baseline))
write_report(output_path + 'change_' + suffix + '.csv', size_columns, convert_file_dict_to_list(change))
write_report(output_path + 'diff_' + suffix + '.csv', diff_columns, diff)