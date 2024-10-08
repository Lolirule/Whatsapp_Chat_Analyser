import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extractor = URLExtract()
import emoji
def fetch_stats(selected_user,df):
# For extracting the urls


    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages= df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    #Fetch number of media ommited
    num_media = df[df['message']== 'Pictures/Documents\n'].shape[0]
    links =[]
    # fethc number of links
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    x =df['user'].value_counts().head()
    name = x.index
    count = x.values
    plt.bar(name,count)

    return num_messages,len(words),num_media,links

def most_busy_users(df):
    x =df['user'].value_counts().head()
    percentage = round((df['user'].value_counts()/df.shape[0])*100,2)
    return x,percentage
def create_cloud(selected_user,df):
        f= open('hinglish.txt','r')
        stop_words = f.read()
        cleaned_df=df[df['message'] != 'Lengthy Message\n']
        cleaned_df=cleaned_df[cleaned_df['message'] != 'Missed voice call\n']
        cleaned_df=cleaned_df[cleaned_df['message'] != '<Media omitted>\n']
        cleaned_df = cleaned_df[cleaned_df['message'] != 'Pictures/Documents\n']
        if selected_user != 'Overall':
            cleaned_df = cleaned_df[cleaned_df['user'] == selected_user]

        # Removing stop_words
        def remove_stop_words(message):
            y = []
            for word in message.lower().split():
                if word not in stop_words:
                    y.append(word)
            return " ".join(y)
        wc = WordCloud(width =500,height=500,min_font_size = 10,background_color = 'white')
        cleaned_df['message']= cleaned_df['message'].apply(remove_stop_words)
        df_wc = wc.generate(cleaned_df['message'].str.cat(sep = " "))
        return df_wc
def most_common_words(selected_user,df):
    f= open('hinglish.txt','r')
    stop_words = f.read()
    cleaned_df=df[df['message'] != 'Lengthy Message\n']
    cleaned_df=cleaned_df[cleaned_df['message'] != 'Missed voice call\n']
    cleaned_df=cleaned_df[cleaned_df['message'] != '<Media omitted>\n']
    cleaned_df = cleaned_df[cleaned_df['message'] != 'Pictures/Documents\n']
    cleaned_df = cleaned_df[cleaned_df['user'] != 'group_notification\n']
    df= cleaned_df
    if selected_user != 'Overall':
        cleaned_df = cleaned_df[cleaned_df['user'] == selected_user]
    words= []

    for message in cleaned_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message  if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_time_line(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df['datetime'].dt.month
    timeline = (df.groupby(['year','month_num','month'])).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['date'] = df['datetime'].dt.date
    daily_timeline = df.groupby('date').count()['message'].reset_index()

    return daily_timeline

def day_timeline(selected_user,df):
     df['day_name'] = df['datetime'].dt.day_name()

     day_timeline = df.groupby(['day_name','user']).count()['message'].reset_index()


     day_dict = {
     "Monday": 0,
     "Tuesday": 1,
     "Wednesday": 2,
     "Thursday": 3,
     "Friday": 4,
     "Saturday": 5,
     "Sunday": 6
     }

    # We are calculating the days
     days=[]
     day_timeline = day_timeline[day_timeline['user'] != 'group_notification']
     # days give us the unsorted order of days given in the dataframe day_timeline
     for day in day_timeline['day_name']:
        days.append(day)


    # here we are taking the order_list and trying to reorder the days from mon to sunday
     order_list=[]
     for day in days:
        order_list.append(day_dict[day])

     ## for ordering the days Mon-Sunday in the daily_timeline_df
     day_timeline['order'] = order_list

     day_timeline = day_timeline.sort_values(by='order')
    # This is for getting the user names
     unique_users = day_timeline['user'].unique()

     users=[]
    # For filling in the users
     for user in unique_users:
         users.append(user)

    # Here we calculate the number of messages each user has messaged on aparticular day
     user1= day_timeline[day_timeline['user'] == users[0]]
     user2 = day_timeline[day_timeline['user'] == users[1]]

     user1_score =[]
     user2_score =[]
     for message in user1['message']:
         user1_score.append(message)



     for message in user2['message']:
        user2_score.append(message)

     ordered_day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

     return day_timeline,user1_score,user2_score,users,ordered_day_names

def day_timeline_individual(selected_user,df):
    df = df[df['user'] == selected_user]
    df['day_name'] = df['datetime'].dt.day_name()
    day_timeline = df.groupby(['day_name','user']).count()['message'].reset_index()

    day_dict = {
     "Monday": 0,
     "Tuesday": 1,
     "Wednesday": 2,
     "Thursday": 3,
     "Friday": 4,
     "Saturday": 5,
     "Sunday": 6
    }
    days=[]
    day_timeline = day_timeline[day_timeline['user'] != 'group_notification']
     # days give us the unsorted order of days given in the dataframe day_timeline
    for day in day_timeline['day_name']:
       days.append(day)
     # here we are taking the order_list and trying to reorder the days from mon to sunday
    order_list=[]
    for day in days:
       order_list.append(day_dict[day])

     ## for ordering the days Mon-Sunday in the daily_timeline_df
    day_timeline['order'] = order_list

    day_timeline = day_timeline.sort_values(by='order')
    # This is for getting the user names
    unique_users = day_timeline['user'].unique()

    users=[]
    # For filling in the users
    for user in unique_users:
        users.append(user)

    # Here we calculate the number of messages each user has messaged on aparticular day
    user1= day_timeline[day_timeline['user'] == users[0]]
    user1_score =[]
    for message in user1['message']:
        user1_score.append(message)
    ordered_day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return day_timeline,user1_score,users,ordered_day_names

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df= df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df= df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    activity_heatmap = df.pivot_table(index = 'day_name',columns = 'period' , values = 'message',aggfunc = 'count').fillna(0)
    return activity_heatmap