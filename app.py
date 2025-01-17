import streamlit as st
import Preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Sidebar title and file uploader
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")

# If a file is uploaded, read and process it
if uploaded_file is not None:
    # Read file content as bytes and decode to UTF-8
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the chat data
    df = Preprocessor.preprocess(data)

    # Extract unique users (excluding group notifications) and prepare list for selection
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')  # Insert 'Overall' at the top of the list

    # Select user from dropdown
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # If 'Show Analysis' button is clicked
    if st.sidebar.button("Show Analysis"):

        # Fetch statistics (number of messages, words, media, and links)
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        # Display top statistics
        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)

        # Display total messages in first column
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        # Display total words in second column
        with col2:
            st.header("Total Words")
            st.title(words)

        # Display total media messages in third column
        with col3:
             st.header("Total Media Messages")
             st.title(num_media)

        ## Monthly Timeline Section
        st.title("Monthly Timeline")
        timeline = helper.monthly_time_line(selected_user, df)

        # If only one month of data is available, plot a bar chart
        if len(timeline) == 1:
            month_str = timeline['time'][0]  # Get month string (e.g., May-2022)
            message_count = timeline['message'][0]  # Extract message count

            # Create bar chart for the single month
            fig, ax = plt.subplots()
            ax.bar(month_str, message_count, color='brown')

            # Set titles and labels
            ax.set_title(f"Messages in {month_str}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Messages")

            # Show the bar plot
            st.pyplot(fig)

        # If multiple months are available, plot a line chart
        else:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')  # Rotate x-axis labels for better readability
            plt.show()
            st.pyplot(fig)

        ## Daily Timeline Section
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        # If there's only one day's data, plot a bar chart
        if len(daily_timeline) == 1:
            date_str = daily_timeline['date'][0].strftime('%Y-%m-%d')  # Format date to 'YYYY-MM-DD'
            message_count = daily_timeline['message'][0]  # Get the message count

            # Create bar chart for the single date
            fig, ax = plt.subplots()
            ax.bar(date_str, message_count, color='brown')

            # Set titles and labels
            ax.set_title(f"Messages on {date_str}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Messages")

            # Show the bar plot
            st.pyplot(fig)

        # If multiple days are available, plot a line chart
        else:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['date'], daily_timeline['message'], color='brown')
            plt.xticks(rotation='vertical')  # Rotate x-axis labels for better readability
            plt.show()
            st.pyplot(fig)

        ## Finding the busiest users in the group (Group level analysis)

        if selected_user == 'Overall':  # Group-level analysis

            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)

            # Plot the busiest users
            fig, ax = plt.subplots()
            col1, col2, col3 = st.columns(3)

            with col1:
                plt.figure(figsize=(5, 8))  # Set figure size
                ax.bar(x.index, x.values)  # Plot bar chart of busy users
                plt.xticks(rotation='vertical')  # Rotate x-axis labels
                st.pyplot(fig)

            with col2:
                plt.figure(figsize=(5, 8))
                st.dataframe(new_df)  # Display the new dataframe (busy users)

            # If there are exactly 2 users (excluding group notifications), plot comparison
            if len(df['user'].unique()) == 3:
                day_df, user1_score, user2_score, users, ordered_day_names = helper.day_timeline(selected_user, df)

                # Create a bar plot to compare the activity of two users
                fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size

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
                ax.set_xticks(positions1 + bar_width / 2)  # Set the x-ticks between the two bars
                ax.set_xticklabels(ordered_day_names, rotation=45)  # Add day labels with rotation
                ax.legend()

                plt.tight_layout()  # Adjust layout to prevent clipping of labels
                plt.show()
                st.pyplot(fig)

        ## Weekly Activity Section
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        # Display the busiest day
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user, df)

            # Plot the most busy day
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            st.pyplot(fig)

        # Display the busiest month
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)

            # Plot the most busy month
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='pink')
            plt.xticks(rotation='vertical')  # Rotate x-axis labels
            st.pyplot(fig)

        ## Weekly Activity Heatmap
        st.title("Weekly Activity Map")
        activity_heat_map = helper.activity_heatmap(selected_user, df)

        # Plot the activity heatmap
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heat_map)
        st.pyplot(fig)

        ## Word Cloud Section
        st.title("Word Cloud")
        df_wc = helper.create_cloud(selected_user, df)

        # Display the word cloud
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        ## Most Common Words Section
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        # Plot the most common words
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])  # Horizontal bar chart
        plt.xticks(rotation='vertical')  # Rotate x-axis labels
        st.pyplot(fig)

        ## Emoji Analysis Section
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        # Display emojis count if available
        col1, col2 = st.columns(2)
        if not emoji_df.empty:
            st.write("Emojis Count")
            with col1:
                st.dataframe(emoji_df)  # Display emoji dataframe
            with col2:
                fig, ax = plt.subplots()
                ax.bar(emoji_df[0].head(), emoji_df[1].head())  # Plot top emojis
                st.pyplot(fig)
        else:
            st.markdown("No emojis found")
