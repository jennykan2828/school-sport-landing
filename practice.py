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

# import datetime as dt

# now = dt.datetime.now()
# yesterday = dt.datetime(2026, 11, 5)
# print(now.strftime('Year: strftime("%Y")'))
# print(now.strftime('Month: strftime("%m")'))
# print(now.strftime('Day: strftime("%d")'))

import datetime


class Student:
    def __init__(
        self, name, age, gender, birth_date, math_grade, eng_grade, chinese_grade
    ):
        self.name = name
        self.age = age
        self.gender = gender
        self.birth_date = birth_date  # should be a datetime.date object
        self.math_grade = math_grade
        self.eng_grade = eng_grade
        self.chinese_grade = chinese_grade

    def math(self):
        return self.math_grade

    def eng(self):
        return self.eng_grade

    def chinese(self):
        return self.chinese_grade

    def calc_age(self):
        """Compute age from birth_date."""
        today = datetime.date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def is_age_correct(self):
        """Check whether stored age matches computed age."""
        return self.age == self.calc_age()


# Create a student — birth_date as a real date object
abc = Student(
    name="jenny",
    age=25,
    gender="F",
    birth_date=datetime.date(2000, 11, 6),
    math_grade=88,
    eng_grade=92,
    chinese_grade=85,
)

print("Name:", abc.name)
print("Stored age:", abc.age)
print("Computed age:", abc.calc_age())
print("Age correct?", abc.is_age_correct())
print("Math grade:", abc.math())
print("English grade:", abc.eng())
print("Chinese grade:", abc.chinese())
