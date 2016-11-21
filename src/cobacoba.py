with open("dataset/stopwords.txt", "r") as ins:
    unusedWords = []
    for line in ins:
        unusedWords.append(line)

    # for data in unusedWords:
    # 	print (data)

    word = [('om', u'ADJ', 2), ('in', u'ADJ', 2), ('cepat', u'ADJ', 2), ('sabar', u'ADJ', 2), ('lain', u'ADJ', 2), ('asal', u'ADJ', 2), ('lembang', u'ADJ', 1)]

    for data in word:
    	for data2 in unusedWords:
    		if data[0] == data2:
    			word.remove(data)

    for data in word:
    	print data[0]  		







    print ('setelah unused word dibuang')
    with open("dataset/stopwords.txt", "r") as ins:
    unusedWords = []
    for line in ins:
        unusedWords.append(line)

    for data in word:
        for data2 in unusedWords:
            if data[0] == data2:
                word.remove(data)

    for data in word:
        print data[0]    