df = pandas.read_csv('./src/quiz_questions.csv', index_col=0)
d = df.to_dict()
questions = pandas.DataFrame(d)
questions = questions.sample(n=20)
    # revisit this later - hurting my head!
    #for q in questions:
        #print(questions.iloc[1])
        #user_answer = input("Answer: ")
        #n += n