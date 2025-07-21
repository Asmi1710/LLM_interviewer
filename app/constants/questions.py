
def introductory_question(name):
    return f'Hello {name}. This is a recruitment call for conducting the telephonic interview. How are you doing today?'


python_questions = [{
        'question': 'What is Importance of indentation in Python?',
        'expected_answer': 'In Python, it is very important to indent the code in a specific order. A Python interpreter can be informed that a group of statements belongs to a specific block of code by using Python indentation.'
    },
    {
        'question': 'What is a dynamically typed language and whether Python is one of them?',
        'expected_answer': 'In a dynamically typed language, the data type of a variable is determined at runtime, not at compile time. No need to declare data types manually; Python automatically detects it based on the assigned value.'
    },
    {
        'question': 'What is pass in Python?',
        'expected_answer': 'The pass statement is a placeholder that does nothing. It is used when a statement is syntactically required but no code needs to run. Commonly used when defining empty functions, classes or loops during development.'
    },
    {
        'question': 'How is Exceptional handling done in Python?',
        'expected_answer': f"""There are 3 main keywords i.e. try, except and finally which are used to catch exceptions:
            try: A block of code that is monitored for errors.
            except: Executes when an error occurs in the try block.
            finally: Executes after the try and except blocks, regardless of whether an error occurred. It’s used for cleanup tasks."""
    },
    {
        'question': 'What is List Comprehension in Python?',
        'expected_answer': 'List comprehension is a way to create lists using a concise syntax. It allows us to generate a new list by applying an expression to each item in an existing iterable (such as a list or range). This helps us to write cleaner, more readable code compared to traditional looping techniques.'
    }]

nodejs_questions = ['']

reactjs_questions = ['']

questions_list = {
    'python': python_questions,
    'nodejs': nodejs_questions,
    'reactjs': reactjs_questions
}
