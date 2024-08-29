from datetime import datetime, timedelta

def adjust_srt_timestamps(file_path, adjustment):
    def parse_timecode(timecode):
        # Parse the timecode, ensuring only the first 3 digits of milliseconds are considered
        return datetime.strptime(timecode.strip(), '%H:%M:%S,%f')

    def format_timecode(timecode):
        # Format the datetime back to the correct SRT format
        return timecode.strftime('%H:%M:%S,%f')[:-3]

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    adjusted_lines = []
    for line in lines:
        if '-->' in line:
            start, end = line.split(' --> ')
            try:
                start_time = parse_timecode(start) - timedelta(seconds=adjustment)
                end_time = parse_timecode(end) - timedelta(seconds=adjustment)
            except ValueError:
                print(f"Error parsing timecodes: {start} or {end}")
                continue
            adjusted_line = f"{format_timecode(start_time)} --> {format_timecode(end_time)}\n"
            adjusted_lines.append(adjusted_line)
        else:
            adjusted_lines.append(line)

    new_file_path = file_path.replace('.srt', '_adjusted.srt')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(adjusted_lines)

    print(f"Adjusted file saved as {new_file_path}")

# Example usage
adjust_srt_timestamps('example.srt', 5)  # Adjusting timestamps by 5 seconds
