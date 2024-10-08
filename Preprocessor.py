import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    messages = re.split(pattern,data)[1:]
    print(messages)
    dates = re.findall(pattern,data)
    for i in range(len(dates)):
        string =""
        date_split = dates[i].split(' ')
        string += date_split[0]
    # print(string)
    #print(date_split)
    # Getting the time part
        time = date_split[1]
        num =""
        remaining_part = ""
        if 'PM' in time:
            # print(time)
            for j in range(len(time)):
                if (time[j] != ':'):
                    num += time[j]
                else:
                    num = int(num)
                    num = (num+12) % 24
                    remaining_part = time[j:]
                    remaining_part = remaining_part.replace("PM","")
                    if num==0:
                        num = "00"
                    num =  " " + str(num) + remaining_part
                    break
            string += num
            string += date_split[2] + date_split[3]
            print(len(string),string)
            dates[i] = string
        else:
            # print("AM",dates[i])
            dates[i]= dates[i].replace('AM','')
            dates[i]= dates[i].replace(' -','-')
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].str.strip()
    # Define a regular expression pattern to extract date and time components
    pattern1 = r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2})'

    # Extract date and time components using regex
    df[['date', 'time']] = df['message_date'].str.extract(pattern1)

    # Concatenate date and time components into the desired format
    df['datetime'] = pd.to_datetime(df['date'] + ', ' + df['time'], format='%m/%d/%y, %H:%M')

    df.drop(columns=['date', 'time'], inplace=True)
    df.drop(columns = 'message_date',inplace =True,axis=1)
    # Separate users and messages
    users= []
    messages =[]
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]: # user name
            users.append(entry[1])
            messages.append(entry[2])
        else: # if the colon is not there
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'],inplace =True)
    df['year'] = df['datetime'].dt.year
    df['month']= df['datetime'].dt.month_name()
    df['day_of_month'] =df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['month_num'] = df['datetime'].dt.month
    df['date'] = df['datetime'].dt.date
    df['minute'] = df['datetime'].dt.minute
    df['message'] = df['message'].replace('<Media omitted>\n', 'Pictures/Documents\n')
    df['message'] = df['message'].replace('null\n', 'Missed voice call\n')
    df['message'] = df['message'].replace('', 'Lengthy Message\n')

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period



    return df
