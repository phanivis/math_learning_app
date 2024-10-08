import streamlit as st
import json

st.title("Math Learning App")

# Load problems from JSON file
with open('course_content.json', 'r') as f:
    course_content = json.load(f)

# Define the subject
subjects = ['Mathematics']

# Define topics under Mathematics
topics = ['Multiplication', 'Fractions']

# Initialize session state for navigation and steps
if 'subject' not in st.session_state:
    st.session_state.subject = None
if 'topic' not in st.session_state:
    st.session_state.topic = None
if 'sub_topic' not in st.session_state:
    st.session_state.sub_topic = None
if 'problem_index' not in st.session_state:
    st.session_state.problem_index = None
if 'step' not in st.session_state:
    st.session_state.step = 0

# Create clickable breadcrumbs
st.write("Navigation:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Subjects"):
        st.session_state.subject = None
        st.session_state.topic = None
        st.session_state.sub_topic = None
        st.session_state.problem_index = None
        st.session_state.step = 0
        st.rerun()
with col2:
    if st.session_state.subject and st.button("Topics"):
        st.session_state.topic = None
        st.session_state.sub_topic = None
        st.session_state.problem_index = None
        st.session_state.step = 0
        st.rerun()
with col3:
    if st.session_state.topic and st.button("Sub-topics"):
        st.session_state.sub_topic = None
        st.session_state.problem_index = None
        st.session_state.step = 0
        st.rerun()

# Navigation logic
if not st.session_state.subject:
    st.subheader("Select Subject:")
    for subject in subjects:
        if st.button(subject):
            st.session_state.subject = subject
            st.rerun()
elif not st.session_state.topic:
    st.subheader("Select Topic:")
    for topic in topics:
        if st.button(topic):
            st.session_state.topic = topic
            st.session_state.sub_topic = None
            st.session_state.problem_index = None
            st.rerun()
elif not st.session_state.sub_topic:
    st.subheader("Select Sub-topic:")
    available_sub_topics = list(course_content[st.session_state.topic].keys())
    for sub_topic in available_sub_topics:
        if st.button(sub_topic):
            st.session_state.sub_topic = sub_topic
            st.session_state.problem_index = None
            st.rerun()
elif st.session_state.problem_index is None:
    st.subheader("Select Problem:")
    problems_list = course_content[st.session_state.topic][st.session_state.sub_topic]
    for i, problem in enumerate(problems_list):
        if st.button(f"Problem {i+1}"):
            st.session_state.problem_index = i
            st.rerun()
else:
    # Retrieve the selected problem
    problems_list = course_content[st.session_state.topic][st.session_state.sub_topic]
    problem = problems_list[st.session_state.problem_index]

    # Display the problem
    st.subheader("Problem:")
    if st.session_state.sub_topic == 'Multiplying 3 numbers':
        st.write(f"Multiply these three numbers: {problem['numbers'][0]} × {problem['numbers'][1]} × {problem['numbers'][2]}")
    elif st.session_state.sub_topic == 'Reducing a fraction to 1':
        st.write(f"Reduce this fraction to 1: {problem['numerator']}/{problem['denominator']}")
    elif st.session_state.sub_topic == 'Finding the greatest common divisor':
        st.write(f"Find the greatest common divisor of: {problem['numbers'][0]} and {problem['numbers'][1]}")
    elif st.session_state.sub_topic == 'Multiplying a fraction by 1':
        st.write(f"Multiply this fraction by 1 to get {problem['result']}: {problem['numerator']}/{problem['denominator']}")

    # Define step-by-step instructions for each sub-topic
    if st.session_state.sub_topic == 'Multiplying 3 numbers':
        numbers = problem['numbers']
        steps = [
            "Hint: Parenthesis means times. So 1(2×3) means 1 times 2 times 3.",
            f"Multiply the first two numbers: {numbers[0]} × {numbers[1]} = {numbers[0] * numbers[1]}",
            f"Multiply that result with the third number: {numbers[0] * numbers[1]} × {numbers[2]} = {(numbers[0] * numbers[1]) * numbers[2]}",
            f"Final result is the answer: {(numbers[0] * numbers[1]) * numbers[2]}"
        ]
    elif st.session_state.sub_topic == 'Reducing a fraction to 1':
        numerator = problem['numerator']
        denominator = problem['denominator']
        steps = [
            f"Turn the fraction upside down: {numerator}/{denominator} becomes {denominator}/{numerator}",
            f"Multiply the top numbers (numerators): {numerator} × {denominator} = {numerator * denominator}",
            f"Multiply the bottom numbers (denominators): {denominator} × {numerator} = {denominator * numerator}",
            f"Show the fraction: {numerator * denominator}/{denominator * numerator}",
            "Since the numerator and denominator are equal, the fraction simplifies to 1.",
            "Final answer: 1"
        ]
    elif st.session_state.sub_topic == 'Finding the greatest common divisor':
        a, b = problem['numbers']
        min_num = min(a, b)
        steps = [f"Find the smallest number between {a} and {b}: {min_num}",
                 f"Check numbers from 1 to {min_num} to find common divisors."]
        gcd = 1
        for x in range(1, min_num + 1):
            if a % x == 0 and b % x == 0:
                gcd = x
                steps.append(f"{x} divides both {a} and {b}. Update GCD to {gcd}.")
            else:
                steps.append(f"{x} does not divide both {a} and {b}.")
        steps.append(f"The greatest common divisor is {gcd}")
    elif st.session_state.sub_topic == 'Multiplying a fraction by 1':
        numerator = problem['numerator']
        denominator = problem['denominator']
        result = problem['result']
        steps = [
            f"Given fraction: {numerator}/{denominator}",
            "When a number or fraction is multiplied by 1, the value remains unchanged.",
            f"We need to find a fraction that, when multiplied by {numerator}/{denominator}, gives {result}.",
            f"To do this, we multiply {numerator}/{denominator} by {result}/{result}:",
            f"({numerator} × {result}) / ({denominator} × {result}) = {numerator*result}/{denominator*result}",
            f"This simplifies to: {result}/{denominator}",
            f"Therefore, the fraction to multiply by is: {result}/{denominator}"
        ]
    else:
        steps = ["Instructions for this sub-topic are not available."]

    # Display steps with "Next step" button
    st.subheader("Solution:")
    if st.button('Next step'):
        if st.session_state.step < len(steps):
            st.session_state.step += 1
    if st.session_state.step > 0:
        for i in range(st.session_state.step):
            st.write(steps[i])
    else:
        st.write("Click 'Next step' to see the first step.")

    if st.session_state.step >= len(steps):
        st.write("You have completed all the steps.")

        # Add "Next Problem" button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Problem"):
                if st.session_state.problem_index < len(problems_list) - 1:
                    st.session_state.problem_index += 1
                    st.session_state.step = 0
                    st.rerun()
                else:
                    st.write("This is the last problem in this sub-topic.")

    # Reset button
    with col2:
        if st.button('Reset'):
            st.session_state.step = 0
            st.rerun()

    # Back to Sub-topics button
    if st.button("Back to Sub-topics"):
        st.session_state.sub_topic = None
        st.session_state.problem_index = None
        st.session_state.step = 0
        st.rerun()

# Display navigation breadcrumbs
breadcrumbs = []
if st.session_state.subject:
    breadcrumbs.append(st.session_state.subject)
if st.session_state.topic:
    breadcrumbs.append(st.session_state.topic)
if st.session_state.sub_topic:
    breadcrumbs.append(st.session_state.sub_topic)

st.write(' > '.join(breadcrumbs))