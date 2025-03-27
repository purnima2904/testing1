def run(path):
    import pandas as pd
    from datetime import timedelta
    
    df = pd.read_excel(path)
    
    df['attendance_date'] = pd.to_datetime(df['attendance_date'])
    
    absent_records = df[df['status'] == 'Absent']
    
    absent_records = absent_records.sort_values(['student_id', 'attendance_date'])
    
    streaks = []
    current_streak = None
    
    for i in range(len(absent_records)):
        row = absent_records.iloc[i]

        if (current_streak is None or 
            row['student_id'] != current_streak['student_id'] or 
            (row['attendance_date'] - current_streak['absence_end_date'] > timedelta(days=1))):
            
            if current_streak is not None and current_streak['total_absent_days'] > 3:
                streaks.append(current_streak)
            
            current_streak = {
                'student_id': row['student_id'],
                'absence_start_date': row['attendance_date'],
                'absence_end_date': row['attendance_date'],
                'total_absent_days': 1
            }
        else:
            current_streak['absence_end_date'] = row['attendance_date']
            current_streak['total_absent_days'] += 1

    if current_streak is not None and current_streak['total_absent_days'] > 3:
        streaks.append(current_streak)

    if streaks:
        streak_df = pd.DataFrame(streaks)
        latest_streaks = streak_df.sort_values('absence_end_date').groupby('student_id').last()
        return latest_streaks.reset_index()
    
    return pd.DataFrame()

result = run('data - sample.xlsx')
print(result.to_string(index=False))
