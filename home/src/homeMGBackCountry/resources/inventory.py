from numbers_parser import Document

class Energy:
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name, value):
        self.__dict__[f"_{name}"] = Document(value).sheets[0].tables[0]

if __name__ == "__main__":
    fname = "/Users/gertjan/Documents/energie rekening/energie_tolakkerweg.numbers"
    table = Energy(fname).document
    for row in table.iter_rows(min_row=0, min_col=0, max_row=4, max_col=table.num_cols-1):
        for cell in row:
            print(cell.formatted_value, end = " ")
        print()

