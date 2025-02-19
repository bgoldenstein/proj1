# Your name: Benjamin Goldenstein
# Your student id: 22465106
# Your email: bngold@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): N/A
# If you worked with generative AI also add a statement for how you used it.
# e.g.: 
# Asked Chatgpt hints for debugging and suggesting the general sturcture of the code 

import os
import csv
import unittest

def csv_reader(filename):
    """
    Load employee data from a CSV file.
    """
    employees = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for i in reader:
            id = i["employee_id"]
            employees["employee_id"] = {
                "gender": i["gender"],
                "race": i["race"],
                "hire_year": i["hire_year"]
            }
    return employees
    

def split_by_hire_year(employees, split_year):
    """
    Split employee data into two dictionaries based on hire year.
    """
    before = {}
    after = {}
    for i, j in employees.items():
        if int(j["hire_year"]) < split_year:
            before[i] = j
        else:
            after[i] = j
    return (before, after)

    

def count_race_or_gender(employees):
    """
    Count the number of employees belonging to each race and gender category.
    """
    count = {}
    raceCount = {}
    genderCount = {}

    for i in employees.values():
        race = i["race"]
        gender = i["gender"]
        if race in raceCount:
            raceCount[race] += 1
        else:
            raceCount[race] = 1
        if gender in genderCount:
            genderCount[gender] += 1
        else:
            genderCount[gender] = 1

        count = {"race": raceCount, "gender": genderCount}
        return count

def count_race_and_gender(employees):
    """
    Count the number of employees within each combination of race and gender.
    """
    raceAndGenderCount = {}
    for i, j in employees.items():
        combo = j["race"] + "_" + j["gender"]
        if combo in raceAndGenderCount:
            raceAndGenderCount[combo] += 1
        else:
            raceAndGenderCount[combo] = 1
    return raceAndGenderCount


def csv_writer(data, filename):
    """
    Write data to a CSV file.
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Race&Gender', 'num_employees'])
        for i, j in data.items():
            writer.writerow([i, j])

    pass


def reduce_company_costs(employees, target_reduction):
    """
    EXTRA CREDIT OPTION ONE
    Create your own algorithm to reduce company payroll costs. 
    """
    pass


class TestEmployeeDataAnalysis(unittest.TestCase):

    def setUp(self):
        """
        - Set up any variables you will need for your test cases
        - Feel free to use 'smaller_dataset.csv' for your test cases so that you can verify 
        the correct output. 
        """
        self.testData = {
            "employee_436": {"gender": "Male", "race": "Black", "hire_year": 1957},
            "employee_437": {"gender": "Male", "race": "White", "hire_year": 1963},
            "employee_438": {"gender": "Female", "race": "Black", "hire_year": 1970},
            "employee_439": {"gender": "Male", "race": "White", "hire_year": 1954},
            "employee_440": {"gender": "Male", "race": "Other", "hire_year": 1965},
            "employee_441": {"gender": "Male", "race": "White", "hire_year": 1959}
        }
        self.split_year1 = 1964
        self.split_year2 = 1970
    def test_csv_reader(self):
        # Your test code for csv_reader goes here
        tested = csv_reader("GM_employee_data.csv")
        self.assertGreater(len(tested), 0)
        for i in tested:
            self.assertGreater(len(i), 0)
        for i, j in tested:
            self.assertIn("gender", j)
            self.assertIn("race", j)
            self.assertIn("hire_year", j)           

    def test_split_by_hire_year(self):
        # Your test code for split_by_hire_year goes here
        before, after = split_by_hire_year(self.testData, self.split_year1)
        self.assertCountEqual(len(before), 4)
        self.assertCountEqual(len(after), 2)
        before, after = split_by_hire_year(self.testData, self.split_year2)
        self.assertCountEqual(len(before), 5)
        self.assertCountEqual(len(after), 1)
        

    def test_count_race_or_gender(self):
        # Your test code for count_race_or_gender goes here
        tested = count_race_or_gender(self.testData)
        self.assertEqual(len(tested), 2)
        self.assertCountEqual(tested["race"], {"White": 3, "Black": 2, "Other": 1})
        self.assertCountEqual(tested["gender"], {"Male": 5, "Female": 1})

    def test_count_race_and_gender(self):
        # Your test code for count_race_and_gender goes here
        tested = count_race_and_gender(self.testData)
        self.assertEqual(len(tested), 4)
        
        self.assertEqual(tested, {
            "Black_Male": 1,
            "White_Male": 3,
            "Black_Female": 1,
            "Other_Male": 1
        })
        pass

    def test_reduce_company_costs(self):
        # Your test code for reduce_company_costs goes here
        pass




def main():
    # Load employee data from the CSV file
    employee_data = csv_reader('GM_employee_data.csv')

    # Task 1: Split employees by hire year
    employees_before_1964, employees_after_1964 = split_by_hire_year(employee_data, 1964)
    
    # Task 2: Count employees by race or gender before and after layoffs
    race_gender_counts_total = count_race_or_gender(employee_data)
    race_gender_counts_after_layoffs = count_race_or_gender(employees_before_1964)

    # Task 3: Count employees by race and gender combinations before and after layoffs
    gendered_race_counts_total = count_race_and_gender(employee_data)
    gendered_race_counts_after_layoffs = count_race_and_gender(employees_before_1964)

    # Print and interpret the results
    print("Analysis Results:")
    print("--------------------------------------------------------")

    # Task 1: Splitting employees
    print("Task 1: Split Employees by Hire Year")
    print(f"Number of employees hired total: {len(employee_data)}")
    print(f"Number of employees after layoffs: {len(employees_before_1964)}")
    print("--------------------------------------------------------")

    # Task 2: Comparing race or gender of all employees before and after layoffs
    print("Task 2: Comparing Race and Gender Before and After Layoffs")
    print("Category: Before Layoffs ---> After Layoffs")
    print("Race:")
    for category, count_before in race_gender_counts_total['race'].items():
        count_after = race_gender_counts_after_layoffs['race'].get(category, 0)
        print(f"\t{category}: {count_before} ---> {count_after}")

    print("Gender:")
    for category, count_before in race_gender_counts_total['gender'].items():
        count_after = race_gender_counts_after_layoffs['gender'].get(category, 0)
        print(f"\t{category}: {count_before} ---> {count_after}")

    print("--------------------------------------------------------")

    # Task 3: Comparing race and gender combinations before and after layoffs
    print("Task 3: Comparing Gendered Race Combinations Before and After Layoffs")
    print("Category: Before Layoffs ---> After Layoffs")
    print("Gendered races:")
    for category, count_before in gendered_race_counts_total.items():
        count_after = gendered_race_counts_after_layoffs.get(category, 0)
        print(f"\t{category}: {count_before} ---> {count_after}")

    print("--------------------------------------------------------")

    csv_writer(gendered_race_counts_total, "GM_employee_data_before_layoffs.csv")
    csv_writer(gendered_race_counts_after_layoffs, "GM_employee_data_after_layoffs.csv")



if __name__ == "__main__":
    # Uncomment the following line to run the unittests
    # unittest.main(verbosity=2)
    
    main()

