import datetime


class Student:
    def __init__(
        self, name, age, gender, birth_date, math_grade, eng_grade, chinese_grade
    ):
        self.name = name
        self.age = age
        self.gender = gender
        self.birth_date = birth_date  # datetime.date object
        self.math_grade = math_grade
        self.eng_grade = eng_grade
        self.chinese_grade = chinese_grade

    # ---- grade getters ----
    def math(self):
        return self.math_grade

    def eng(self):
        return self.eng_grade

    def chinese(self):
        return self.chinese_grade

    def average(self):
        return (self.math_grade + self.eng_grade + self.chinese_grade) / 3

    # ---- age helpers ----
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

    # ---- nice printing ----
    def __repr__(self):
        return (
            f"Student(name={self.name!r}, age={self.age}, gender={self.gender!r}, "
            f"math={self.math_grade}, eng={self.eng_grade}, "
            f"chinese={self.chinese_grade})"
        )


class Classroom:
    def __init__(self, class_name):
        self.class_name = class_name
        self.students = []  # list of Student objects

    # ---------- add / delete ----------
    def add_student(self, student):
        """Add a Student. Reject duplicate names (case-insensitive)."""
        if not isinstance(student, Student):
            raise TypeError("add_student() expects a Student instance")
        if self.find_student(student.name) is not None:
            raise ValueError(
                f"Student '{student.name}' already exists in {self.class_name}"
            )
        self.students.append(student)
        print(f"✅ Added {student.name} to {self.class_name}")

    def delete_student(self, name):
        """Delete a student by name. Returns True if removed, False if not found."""
        student = self.find_student(name)
        if student is None:
            print(f"⚠️  Student '{name}' not found in {self.class_name}")
            return False
        self.students.remove(student)
        print(f"🗑️  Removed {student.name} from {self.class_name}")
        return True

    # ---------- lookups ----------
    def find_student(self, name):
        """Find a student by name (case-insensitive). Returns Student or None."""
        name_lower = name.lower()
        for s in self.students:
            if s.name.lower() == name_lower:
                return s
        return None

    def list_students(self):
        """Print a table of all students."""
        if not self.students:
            print(f"({self.class_name} is empty)")
            return
        print(f"\n📋 Students in {self.class_name} ({len(self.students)}):")
        print(
            f"{'Name':<12}{'Age':<6}{'Gender':<8}{'Math':<6}{'Eng':<6}{'Chinese':<8}{'Avg':<6}"
        )
        print("-" * 52)
        for s in self.students:
            print(
                f"{s.name:<12}{s.age:<6}{s.gender:<8}"
                f"{s.math_grade:<6}{s.eng_grade:<6}{s.chinese_grade:<8}"
                f"{s.average():<6.1f}"
            )

    # ---------- stats ----------
    def class_average(self):
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students) / len(self.students)

    def subject_average(self, subject):
        """subject: 'math' | 'eng' | 'chinese'"""
        if not self.students:
            return 0.0
        getter = getattr(self.students[0], subject)
        return sum(getter() for s in self.students) / len(self.students)

    def __len__(self):
        return len(self.students)


# ---------------- Demo ----------------
if __name__ == "__main__":
    # Create the classroom
    cls = Classroom("Class A")

    # Add students
    cls.add_student(Student("jenny", 25, "F", datetime.date(2000, 11, 6), 88, 92, 85))
    cls.add_student(Student("tom", 24, "M", datetime.date(2001, 5, 20), 75, 80, 70))
    cls.add_student(Student("amy", 23, "F", datetime.date(2002, 1, 15), 95, 89, 92))

    # Try adding a duplicate
    try:
        cls.add_student(
            Student("Jenny", 25, "F", datetime.date(2000, 11, 6), 88, 92, 85)
        )
    except ValueError as e:
        print(f"❌ {e}")

    # Show all
    cls.list_students()

    # Delete a student
    cls.delete_student("tom")
    cls.delete_student("nobody")  # not found

    # Show again
    cls.list_students()

    # Stats
    print(f"\nClass average: {cls.class_average():.1f}")
    print(f"Math average:  {cls.subject_average('math'):.1f}")
    print(f"Class size:    {len(cls)}")

    # Individual lookups
    j = cls.find_student("jenny")
    if j:
        print(
            f"\nFound {j.name}: age correct? {j.is_age_correct()}, computed age {j.calc_age()}"
        )
