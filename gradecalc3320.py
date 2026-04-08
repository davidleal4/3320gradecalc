import time

# --- Terminal Colors for Beautiful UI ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Course Weights (Based on Syllabus) ---
WEIGHTS = {
    "Homework 1": 0.05,
    "Homework 2": 0.05,
    "Homework 3": 0.05,
    "Intro Exam (Exam 1)": 0.15,
    "Midterm 1 (Exam 2)": 0.20,
    "Midterm 2": 0.20,
    "Final Exam": 0.30
}

# --- Known Class Averages ---
CLASS_AVERAGES = {
    "Homework 1": 69.4,
    "Intro Exam (Exam 1)": 28.2,
    "Midterm 1 (Exam 2)": 22.0
}

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def get_valid_percentage(prompt_text):
    while True:
        try:
            value = float(input(f"{Colors.CYAN}{prompt_text}{Colors.ENDC}"))
            if 0 <= value <= 200: # Allowing over 100 in case of bonus points
                return value
            else:
                print(f"{Colors.WARNING}Please enter a realistic percentage (0-200).{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input. Please enter a numerical value.{Colors.ENDC}")

def calculate_and_print_results(total_earned, future_assignments, curve, raw_class_avg=None, curved_class_avg=None):
    target_grade = 70.0
    future_weight = sum(future_assignments.values())
    
    points_needed = target_grade - total_earned - curve
    
    if points_needed <= 0:
        min_needed_future = 0.0
    elif future_weight == 0:
        min_needed_future = float('inf') # Impossible if no weight left and points still needed
    else:
        min_needed_future = points_needed / future_weight

    print_header("Results & Projections")
    
    # Only print class averages on the first run
    if raw_class_avg is not None and curved_class_avg is not None:
        print(f"{Colors.BOLD}Class Performance:{Colors.ENDC}")
        print(f"  • Projected Raw Class Average:    {raw_class_avg:.2f}%")
        print(f"  • {Colors.GREEN}Projected Curved Class Average: {curved_class_avg:.2f}%{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Your Current Standing:{Colors.ENDC}")
    print(f"  • Points earned so far:           {total_earned:.2f} / {(1 - future_weight)*100:.1f} possible points")
    print(f"  • Assumed Curve:                  +{curve:.2f}%\n")

    if future_weight == 0:
        final_grade = total_earned + curve
        print(f"{Colors.BOLD}Final Course Outcome:{Colors.ENDC}")
        if final_grade >= 70.0:
            print(f"  {Colors.GREEN}Congratulations! Your simulated final grade is {final_grade:.2f}%, which is passing.{Colors.ENDC}")
        else:
            print(f"  {Colors.FAIL}Unfortunately, your simulated final grade is {final_grade:.2f}%, which is below 70%.{Colors.ENDC}")
        return

    print(f"{Colors.BOLD}The Path to 70% (C-):{Colors.ENDC}")
    if min_needed_future > 100:
        print(f"  {Colors.FAIL}WARNING: You need a minimum of {min_needed_future:.2f}% on your remaining assignments.")
        print(f"  This is mathematically impossible without extra credit.{Colors.ENDC}")
    elif min_needed_future == 0.0:
        print(f"  {Colors.GREEN}Congratulations! You have already secured at least a 70% in the course with the curve.{Colors.ENDC}")
    else:
        print(f"  {Colors.WARNING}To achieve a final grade of 70%, you must score AT LEAST:{Colors.ENDC}")
        print(f"  {Colors.BOLD}{Colors.WARNING}--> {min_needed_future:.2f}% <--{Colors.ENDC}")
        print(f"  on EACH of the following remaining assignments:")
        for assignment in future_assignments:
            print(f"    - {assignment}")
    
    print("\n" + "="*50)

def main():
    print(f"{Colors.BOLD}{Colors.GREEN}")
    print("==================================================")
    print("  COSC 3320: Algorithms & Data Structures         ")
    print("  Final Grade & Curve Calculator                  ")
    print("==================================================")
    print(f"{Colors.ENDC}")
    time.sleep(0.5)

    user_scores = {}
    predicted_class_averages = {}

    # Step 1: Gather User's Previous Grades
    print_header("Step 1: Enter Your Current Grades (0-100%)")
    total_earned_so_far = 0.0
    
    for assignment in ["Homework 1", "Intro Exam (Exam 1)", "Midterm 1 (Exam 2)"]:
        score = get_valid_percentage(f"Your grade for {assignment} (worth {WEIGHTS[assignment]*100:.1f}% of total): ")
        user_scores[assignment] = score
        
        relative_contribution = score * WEIGHTS[assignment]
        total_earned_so_far += relative_contribution
        print(f"  {Colors.GREEN}↳ This adds {relative_contribution:.2f}% to your FINAL course grade.{Colors.ENDC}\n")

    # Step 2: Gather Predicted Class Averages
    print_header("Step 2: Predict Upcoming Class Averages (%)")
    for assignment in ["Homework 2", "Homework 3", "Midterm 2", "Final Exam"]:
        predicted_class_averages[assignment] = get_valid_percentage(f"Predicted class average for {assignment}: ")

    # Step 3: Gather Curve Prediction
    print_header("Step 3: Final Curve")
    curve = get_valid_percentage("Predicted final grade curve to be added (in %, e.g., enter 5 for a 5% curve): ")

    print(f"\n{Colors.BLUE}Calculating your future...{Colors.ENDC}\n")
    time.sleep(1)

    # Initial Class Average Calculations
    current_class_points = sum(CLASS_AVERAGES[a] * WEIGHTS[a] for a in CLASS_AVERAGES)
    future_class_points = sum(predicted_class_averages[a] * WEIGHTS[a] for a in predicted_class_averages)
    raw_final_class_average = current_class_points + future_class_points
    curved_final_class_average = raw_final_class_average + curve

    # Setup tracking for future assignments
    upcoming_assignments = {
        "Homework 2": WEIGHTS["Homework 2"],
        "Homework 3": WEIGHTS["Homework 3"],
        "Midterm 2": WEIGHTS["Midterm 2"],
        "Final Exam": WEIGHTS["Final Exam"]
    }

    # Print Initial Results
    calculate_and_print_results(
        total_earned_so_far, 
        upcoming_assignments, 
        curve, 
        raw_final_class_average, 
        curved_final_class_average
    )

    # Step 4: Interactive Simulation Loop
    while upcoming_assignments:
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== Simulation Mode ==={Colors.ENDC}")
        print("Would you like to simulate a specific grade for an upcoming assignment to see how it changes your requirements?")
        
        assignment_list = list(upcoming_assignments.keys())
        for i, assignment in enumerate(assignment_list, 1):
            print(f"  {i}. Simulate {assignment}")
        print("  0. No, exit calculator")

        choice = input(f"\n{Colors.CYAN}Enter your choice (0-{len(assignment_list)}): {Colors.ENDC}")
        
        try:
            choice_idx = int(choice)
            if choice_idx == 0:
                break
            elif 1 <= choice_idx <= len(assignment_list):
                selected_assignment = assignment_list[choice_idx - 1]
                sim_score = get_valid_percentage(f"Enter your simulated score for {selected_assignment} (0-100%): ")
                
                # Apply the simulation
                sim_weight = upcoming_assignments[selected_assignment]
                relative_contribution = sim_score * sim_weight
                total_earned_so_far += relative_contribution
                
                print(f"\n  {Colors.GREEN}↳ Locking in {sim_score}% for {selected_assignment}. This adds {relative_contribution:.2f}% to your final grade.{Colors.ENDC}\n")
                
                # Remove from upcoming assignments
                del upcoming_assignments[selected_assignment]
                
                # Recalculate
                time.sleep(0.5)
                calculate_and_print_results(total_earned_so_far, upcoming_assignments, curve)
            else:
                print(f"{Colors.FAIL}Invalid choice. Please enter a number from the menu.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input. Please enter a number.{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Calculator exited.{Colors.ENDC}")