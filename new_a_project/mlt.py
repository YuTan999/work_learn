import matplotlib.pyplot as plt

# 假设你已经有了用户评分数据，包含用户和评分属性
user_ratings = [
    ['User1', 4],
    ['User2', 5],
    ['User3', 3],
    ['User3', 4],
    ['User3', 5],
    ['User2', 5],
    ['User4', 3],
    ['User3', 4],
    ['User5', 5],
    ['User2', 5],
    ['User3', 3],
    ['User6', 4],
    ['User3', 5],
    ['User3', 4],
    ['User5', 5],
    ['User2', 5],
    ['User3', 3],
    ['User6', 4],
    ['User3', 5],
]

# 统计每个评分的用户数
ratings_count = {}
for user, rating in user_ratings:
    if user in ratings_count:
        ratings_count[user] += 1
    else:
        ratings_count[user] = 1

# 计算评分占比
total_users = len(user_ratings)
ratings_percentage = {}
for user, count in ratings_count.items():
    percentage = (count / total_users) * 100
    ratings_percentage[user] = percentage

final_count = {}
count_below_10 = 0
count_below_25 = 0
count_below_50 = 0
count_below_100 = 0
for user, percentage in ratings_percentage.items():
    if percentage < 10:
        count_below_10 += 1
    elif percentage >= 10 and percentage < 25:
        count_below_25 += 1
    elif percentage >=25 and percentage < 50:
        count_below_50 += 1
    else:
        count_below_100 +=1

final_count['count_below_10']=count_below_10
final_count['count_below_25']=count_below_25
final_count['count_below_50']=count_below_50
final_count['count_below_100']=count_below_100

print(final_count)
# 按照占比进行排序
# sorted_ratings_percentage = dict(sorted(ratings_percentage.items(), key=lambda x: x[1]))

# 提取数据
ratings = list(final_count.keys())
percentages = list(final_count.values())

# 绘制柱状图
plt.bar(ratings, percentages)
plt.xlabel('Rating')
plt.ylabel('Percentage')
plt.title('User Ratings Percentage')

# 添加标签
for i, percentage in enumerate(percentages):
    plt.annotate(f'{percentage:.2f}%', (i, percentage), ha='center', va='bottom')

plt.show()