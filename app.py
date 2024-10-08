import streamlit as st
import Preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df = Preprocessor.preprocess(data)
#     st.dataframe(df)
    # we are going to fetch Unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
             st.header("Total Media Messages")
             st.title(num_media)
        ## Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_time_line(selected_user,df)
        fig,ax = plt.subplots()

        ax.plot(timeline['time'],timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

        ## Daily Time_line

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(daily_timeline['date'],daily_timeline['message'],color= 'brown')
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

        ## Finding busiest users in the group(Group level)

        if selected_user == 'Overall':

            st.title('Most Busy Users')

            x,new_df= helper.most_busy_users(df)

            fig,ax = plt.subplots()

            col1,col2,col3 = st.columns(3)

            with col1:
                plt.figure(figsize=(5, 8))
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                plt.figure(figsize=(5, 8))
                st.dataframe(new_df)
            if len(df['user'].unique()) == 3:  # Including Group Notification
                day_df, user1_score, user2_score, users, ordered_day_names = helper.day_timeline(selected_user, df)

                # Create a bar plot
                fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size directly in subplots

                # Plot the bars for user 1 and user 2
                bar_width = 0.35  # Set the width of the bars
                positions1 = np.arange(len(ordered_day_names))  # X positions for user1
                positions2 = positions1 + bar_width  # Shift positions for user2

                ax.bar(positions1, user1_score, width=bar_width, label=users[0])
                ax.bar(positions2, user2_score, width=bar_width, label=users[1])

                # Customize the plot
                ax.set_xlabel("Days")
                ax.set_ylabel("Scores")
                ax.set_title(f"{users[0]} vs. {users[1]}")
                ax.set_xticks(positions1 + bar_width / 2)  # Set the x-ticks to be between the two bars
                ax.set_xticklabels(ordered_day_names, rotation=45)  # Add day labels with rotation
                ax.legend()

                plt.tight_layout()  # Adjust layout to prevent clipping of labels
                plt.show()
                st.pyplot(fig)


        # Displaying the overall activity weekly combined

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user,df)

            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'orange')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'pink')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        # Hourly basis on a weekly
        st.title("Weekly Activity Map")
        activity_heat_map = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heat_map)
        st.pyplot(fig)

        # Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_cloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])

        plt.xticks(rotation='vertical')



        st.pyplot(fig)


        # Emoji analysis
        st.title("Emoji Analysis")

        emoji_df = helper.emoji_helper(selected_user,df)

        st.write("Emojis Count")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.bar(emoji_df[0].head(),emoji_df[1].head())
            st.pyplot(fig)
