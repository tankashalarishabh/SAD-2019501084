import csv
def Search():
    inp = "Cold Fire"
        # print(inp)
    with open('books.csv', newline= "") as file:
        readData = [row for row in csv.DictReader(file)]
        for i in range(len(readData)):
            if readData[i]['title'] == inp:
                return readData[i]['isbn'],readData[i]['title'],readData[i]['author'],readData[i]['year']
                    # return render_template("Aftersearch.html",isbn=readData[i]['isbn'],title=readData[i]['title'],author=readData[i]['author'],year=readData[i]['year'])
        return "not found"

print(Search())