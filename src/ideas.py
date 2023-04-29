with open('./src/quiz_questions.csv') as csv_file:
        questions = csv.DictReader(csv_file)
        questions = random.sample(questions.items, 20)



df = pandas.read_csv('./src/quiz_questions.csv', index_col=0)
d = df.to_dict()
questions = pandas.DataFrame(d)
questions = questions.sample(n=20)
    # revisit this later - hurting my head!
    #for q in questions:
        #print(questions.iloc[1])
        #user_answer = input("Answer: ")
        #n += n



def check(password):
    valid_password = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$'
    password_valid = False
    while not password_valid:
        if (re.fullmatch(valid_password, password)):
            password_valid = True
            return
        else:
            print("Password does not meet required format, please try again.")
            password = input("New password: ")