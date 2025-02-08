from moneycontrol import moneycontrol_api as mc

# Fetch the latest news
latest_news = mc.get_latest_news()

# Print the latest news (assuming latest_news is a dictionary)
print("Latest News:")
print(f"Title: {latest_news['Title:']}")
print(f"Link: {latest_news['Link:']}")
print(f"Date: {latest_news['Date:']}")
print('-' * 80)

# Fetch business news
business_news = mc.get_business_news()

# Print business news (assuming business_news is a dictionary)
print("Business News:")
print(f"Title: {business_news['Title:']}")
print(f"Link: {business_news['Link:']}")
print(f"Date: {business_news['Date:']}")
print('-' * 80)

# Fetch general news
general_news = mc.get_news()

# Print general news (assuming general_news is a dictionary)
print("General News:")
print(f"Title: {general_news['Title:']}")
print(f"Link: {general_news['Link:']}")
print('-' * 80)

