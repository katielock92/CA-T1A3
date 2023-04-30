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


#Except error if file goes missing
# confirming that registered users file exists before trying to run login function:
users_file = "./src/registered_users.csv"
try:
    users_file_exists = open(users_file, "r")
    users_file_exists.close()
except FileNotFoundError as e:
    users_file_exists = open(users_file, "w")
    users_file_exists.write("user_email", "user_password", "user_id\n")
    users_file_exists.close()
