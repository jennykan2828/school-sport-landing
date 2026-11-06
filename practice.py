# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# l4 = [ '*' if i % 2 == 0 else i for i in l]
# print(l4)

# l2 = [i for i in l if i % 2 == 0]
# print(l2)

# import calendar

# year_list = input("enter year list: ")
# year_list = year_list.strip().split(',')
# year_list = [int(i) for i in year_list]

# for year in year_list:
#     print(calendar.isleap(year))

# def bmi(kg, m):
#     bmi = kg / (m * m)
#     status = "underweight" if bmi < 18.5 else "normal" if bmi < 25 else "overweight"
#     return bmi, status

# weight = float(input("Enter your weight in kg: "))
# height = float(input("Enter your height in meters: "))


# bmi, status = bmi(weight, height)
# print(f"Your BMI is {bmi} and your status is {status}.")
# foot = ['rice', 'orange', 'apple', 'banana', 'pear', 'strawberry', 'mango', 'pineapple', 'grape', 'kiwi']
# foot_set=set(foot)
# print(foot_set)

import datetime as dt

now = dt.datetime.now()
yesterday = dt.datetime(2026, 11, 5)
print(now.strftime('Year: strftime("%Y")'))
print(now.strftime('Month: strftime("%m")'))
print(now.strftime('Day: strftime("%d")'))
