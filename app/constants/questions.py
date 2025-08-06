
def introductory_question(name):
    return f'Hello {name}. This is a recruitment call for conducting the telephonic interview. For each question, you will have 20 to 30 seconds to finish your reply. Please let me know if you are ready to start the interview.'


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

nodejs_questions = [
    {
        'question': 'Why is NodeJS single-threaded?',
        'expected_answer': "NodeJS is single-threaded because it's based on the asynchronous, non-blocking nature of JavaScript. This design makes it simpler to develop and maintain, and it allows NodeJS to handle many concurrent requests efficiently."
    },
    {
        'question': 'What is middleware?',
        'expected_answer': "Middleware is the function that works between the request and the response cycle. Middleware gets executed after the server receives the request and before the controller sends the response."
    },
    {
        'question': 'What do you mean by event loop in NodeJS?',
        'expected_answer': "The event loop in NodeJS is a mechanism that allows it to handle multiple asynchronous tasks concurrently within a single thread. It continuously listens for events and executes associated callback functions."
    },
    {
        'question': 'What is a buffer in NodeJS?',
        'expected_answer': "The Buffer class in NodeJS is used to perform operations on raw binary data. Generally, Buffer refers to the particular memory location in memory. Buffer and array have some similarities, but the difference is that array can be any type, and it can be resizable. Buffers only deal with binary data, and it can not be resizable. Each integer in a buffer represents a byte. console.log() function is used to print the Buffer instance."
    },
    {
        'question': 'What is callback hell?',
        'expected_answer': "Callback hell is an issue caused by a nested callback. This causes the code to look like a pyramid and makes it unable to read To overcome this situation, we use promises."
    },
    ]

reactjs_questions = [{
        'question': 'What is virtual DOM in React?',
        'expected_answer': "The Virtual DOM in React is an in-memory representation of the actual DOM. It helps React efficiently update and render the user interface by comparing the current and previous virtual DOM states using a process called diffing."
    },
    {
        'question': 'What are components in React?',
        'expected_answer': "A Component is one of the core building blocks of React. In other words, we can say that every application you will develop in React will be made up of pieces called components. Components make the task of building UIs much easier. "
    },
    {
        'question': 'Explain props in React?',
        'expected_answer': "React allows us to pass information to a Component using something called props (which stands for properties). Props are objects which can be used inside a component. We can access any props inside from the component’s class to which the props is passed. The props can be accessed as : this.props.propName;"
    },
    {
        'question': 'What are Pure Components in React?',
        'expected_answer': "A Pure Component is a type of React component that only re-renders if the props or state it receives change. React provides React.PureComponent, which is a base class that automatically performs a shallow comparison of props and state to determine if a re-render is necessary."
    },
    {
        'question': 'What is React Router?',
        'expected_answer': "React Router is a standard library for routing in React. It enables the navigation among views of various components in a React Application, allows changing the browser URL, and keeps the UI in sync with the URL."
    },
    ]

questions_list = {
    'python': python_questions,
    'nodejs': nodejs_questions,
    'reactjs': reactjs_questions
}
