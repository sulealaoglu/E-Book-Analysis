import bs4
import requests


def removeStopWords(allWords):
    cleanWords = []
    symbols = ['1', '2', '4', '5', '6', '7', '8', '9', '0', '\\', '{', '}', '!', '^', '%', '&',
               '/', '(', ')', '=', '?', '´', '$', '_', ',', '.', ':', ';', '*', '[', ']', '#', '>',
               '<', '|', '-', "'", '"']
    for word in allWords:  # remove symbols in words
        for char in symbols:
            if char in word:
                while char in word:
                    word = word.replace(char, " ")
                    # word = word.strip()
        if " " in word:
            list = word.split()
            cleanWords += list
        else:
            if len(word) > 0:
                cleanWords.append(word)

    clean2Words = []
    stopWords = ['i', 'me', 'my', 'myself', '3', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                 "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                 "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
                 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                 'doing',
                 'a', 'an', 'the', 'and', 'but','would', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
                 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
                 'below',
                 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'value', 'under', 'again', 'further',
                 'then',
                 'once',
                 'here', 'there', 'when', 'where', 'why',"within","also" 'panel', 'first', 'use', 'how', 'all', 'any', 'both', 'each',
                 'few', 'more', 'most',
                 'other',
                 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'k',
                 'pim',
                 'can',
                 'will', 'just', 'do', "don't", 'should', "should've", 'now', 'd', 'b', 'r', 'll', 'm', 'o', 're', 've',
                 'y', 'aint',
                 'are', "aren't", 'could', "couldn't", 'did', "didn't", 'does', "doesn't", 'had', "hadn't", 'has',
                 "hasn't", 'haven', "haven't", 'is', "isn't", 'might', "mightn't", 'must', "mustn't", 'need',
                 "needn't", 'should', "shouldn't", 'was', "wasn't", 'were', "weren't", 'name', 'line', 'next', '`',
                 "won't",
                 "wouldn't"]
    for word in cleanWords:  # removing stop  words
        counter = 0
        for stop in stopWords:
            if stop == word:
                counter += 1
        if counter == 0:
            clean2Words.append(word)

    return clean2Words


def wordFrequency(allwords):
    words = {}
    for word in allwords:  # calculate the frequency of each word
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

    wanted_str = list(words.keys())
    wanted_num = list(words.values())
    for i in range(len(wanted_num)):  # sorting words in descending order
        for j in range(0, len(wanted_num)):
            if wanted_num[i] > wanted_num[j]:
                wanted_num[i], wanted_num[j] = wanted_num[j], wanted_num[i]
                wanted_str[i], wanted_str[j] = wanted_str[j], wanted_str[i]
    final_lst = []
    for k in range(len(wanted_num)):  # adding word and frequency side by side
        final_lst.append(wanted_str[k])
        final_lst.append(wanted_num[k])

    return final_lst


def downloadBook(bookName):  # download the book on the internet
    bookUrl = bookName.replace(" ", "_")

    link = "https://en.wikibooks.org/wiki/" + bookUrl + "/Print_version"
    r = requests.get(link)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    file = open(bookName + ".txt", "w")  # create a text file for writing book
    for i in soup.find_all(class_="mw-parser-output"):
        file.write(i.text.encode('utf8').decode('ascii', 'ignore'))  # for special characters use utf8
        file.close()
    f = open(bookName + ".txt", "r")  # open and read book.txt file
    text = f.read()
    f.close()
    if len(text)<1:  # for book links starting with a lowercase p
        link = "https://en.wikibooks.org/wiki/" + bookUrl + "/print_version"
        r = requests.get(link)
        soup = bs4.BeautifulSoup(r.content, "lxml")
        file = open(bookName + ".txt", "w")  # create a text file for writing book
        for i in soup.find_all(class_="mw-parser-output"):
            file.write(i.text.encode('utf8').decode('ascii', 'ignore'))  # for special characters use utf8
            file.close()



def clearBook(bookName):  # read book.txt file,and extract it into words
    f = open(bookName + ".txt", "r")  # open and read book.txt file
    text = f.read()
    f.close()
    text = text.lower()
    allWords = text.split()  # converting string to list as word by word
    finalWords = removeStopWords(allWords)  # cleaning stop words and symbols
    wordFreq=wordFrequency(finalWords)
    return wordFreq


def printFrequency(bookName):  # print words with them frequencies on screen
    wordFreq = clearBook(bookName)
    print('NO          WORDS             FREQ_1')

    for i in range(0, printLimit * 2, 2):
        if len(wordFreq[i]) < 17:
            spaceNumber = 17 - len(wordFreq[i])  # space control for organize output on the screen
            space = spaceNumber * " "
            no = (i // 2) + 1
            if no < 10:
                space2 = " " * 9

            else:
                space2 = " " * 8
            print(no, space2, wordFreq[i], space, wordFreq[i + 1])


def compareBooks(book_1, book_2):
    wordFreq = clearBook(book_1)
    wordFreq2 = clearBook(book_2)
    distinctWords1 = []
    distinctWords2 = []
    commonWords_str = []
    commonWords_num_1 = []
    commonWords_num_2 = []
    commonWords_freqsum = []

    if len(wordFreq) > len(wordFreq2):
        n = len(wordFreq2)
    else:
        n = len(wordFreq)
    for i in range(0, n - 1, 2):  # distinct first book
        counter = 0
        for j in range(0, len(wordFreq2), 2):
            if wordFreq[i] == wordFreq2[j]:
                counter += 1

        if counter == 0:
            distinctWords1.append(wordFreq[i])  # words which is in the first book, not in the second
            for k in range(0, len(wordFreq), 2):
                if wordFreq[k] == wordFreq[i]:
                    distinctWords1.append(wordFreq[k + 1])  # number of distinct word in first book


        else:
            commonWords_str.append(wordFreq[i])  # common words
            for m in range(0, len(wordFreq) - 1, 2):
                if wordFreq[m] == wordFreq[i]:
                    commonWords_num_1.append(wordFreq[m + 1])  # number of common word in first book
                    break
            for k in range(0, len(wordFreq2), 2):
                if wordFreq2[k] == wordFreq2[i]:
                    commonWords_num_2.append(wordFreq2[k + 1])  # number of common word in second book
                    break
            sum = wordFreq[m + 1] + wordFreq2[k + 1]
            commonWords_freqsum.append(sum)

    for i in range(len(commonWords_num_1)):  # sorting common words
        for j in range(0, len(commonWords_num_1)):
            if commonWords_freqsum[i] > commonWords_freqsum[j]:
                commonWords_freqsum[i], commonWords_freqsum[j] = commonWords_freqsum[j], commonWords_freqsum[i]
                commonWords_num_1[i], commonWords_num_1[j] = commonWords_num_1[j], commonWords_num_1[i]
                commonWords_num_2[i], commonWords_num_2[j] = commonWords_num_2[j], commonWords_num_2[i]
                commonWords_str[i], commonWords_str[j] = commonWords_str[j], commonWords_str[i]
    final_lst = []
    for k in range(len(commonWords_num_1)):  # append common word,number of words in first book and second book
        final_lst.append(commonWords_str[k])
        final_lst.append(commonWords_num_1[k])
        final_lst.append(commonWords_num_2[k])
        final_lst.append(commonWords_freqsum[k])

    for i in range(0, len(wordFreq2), 2):  # distinct second book
        counter = 0
        for j in range(0, len(wordFreq), 2):
            if wordFreq2[i] == wordFreq[j]:
                counter += 1

        if counter == 0:
            distinctWords2.append(wordFreq2[i])  # words which is in the second book, not in the first book
            for k in range(0, len(wordFreq2), 2):
                if wordFreq2[k] == wordFreq2[i]:
                    distinctWords2.append(wordFreq2[k + 1])  # number of distinct word in second book

    print()
    print("COMMON WORDS:")  # print common words on screen
    print('NO          WORDS               FREQ_1           FREQ_2          FREQ_SUM')
    for i in range(0, printLimit * 4, 4):
        if len(commonWords_str[i]) < 19:  # space control for organize output on the screen
            spaceNumber = 19 - len(final_lst[i])
            space = spaceNumber * " "
        no = (i // 4) + 1
        if no < 10:
            space2 = " " * 9
        else:
            space2 = " " * 8
        if final_lst[i + 1] > 99:
            space3 = 12 * " "
        else:
            space3 = 13 * " "
        if final_lst[i + 2] > 99:
            space4 = 12 * " "
        else:
            space4 = 13 * " "

        print(no, space2, final_lst[i], space, final_lst[i + 1], space3, final_lst[i + 2], space4, final_lst[i + 3])
    print()
    print("Book:" + book1_name)
    print("DISTINCT WORDS:")  # print first book's distinct words on screen
    print('NO          WORDS               FREQ_1')
    for i in range(0, printLimit * 2, 2):
        if len(distinctWords1[i]) < 19:  # space control for organize output on the screen
            spaceNumber = 19 - len(distinctWords1[i])
            space = spaceNumber * " "
            no = (i // 2) + 1
            if no < 10:
                space2 = " " * 9
            else:
                space2 = " " * 8
        no = (i // 2) + 1
        print(no, space2, distinctWords1[i], space, distinctWords1[i + 1])
    print()
    print("Book:" + book2_name)  # print second book's distinct words on screed
    print("DISTINCT WORDS:")
    print('NO          WORDS               FREQ_2')
    for i in range(0, printLimit * 2, 2):
        if len(distinctWords2[i]) < 19:
            spaceNumber = 19 - len(distinctWords2[i])
            space = spaceNumber * " "
            no = (i // 2) + 1
            if no < 10:
                space2 = " " * 9

            else:
                space2 = " " * 8
            print(no, space2, distinctWords2[i], space, distinctWords2[i + 1])


# getting user input
global printLimit
number = int(input("How many books do you want to review?: "))
if number != 1 and number != 2:
    flag = True
    while flag:
        print("Please choose only one book or two books!")
        number = int(input("How many books do you want to review? "))
        if number == 1 or number == 2:
            break

if number == 1:
    name = input("Please enter book name: ")
    print("Downloading....")
    downloadBook(name)
    printLimit = input("How many word frequencies do you want to see?: ")
    if printLimit=='' or int(printLimit)<=0:
        printLimit=20
    else:
        printLimit=int(printLimit)
    print("Calculating...")
    printFrequency(name)
elif number == 2:
    book1_name = input("Please enter first book's name: ")
    book2_name = input("Please enter second book's name: ")
    print("Downloading...")
    downloadBook(book1_name)
    downloadBook(book2_name)
    printLimit = input("How many word frequencies do you want to see?: ")

    if printLimit == '' or int(printLimit) <= 0:
        printLimit = 20
    else:
        printLimit = int(printLimit)
    print("Calculating...")
    compareBooks(book1_name, book2_name)
