class Energy:

    def __init__(self, doc):
        self.doc = doc

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        from numbers_parser import Document
        self._doc = Document(doc).sheets[0].tables[0]

if __name__ == "__main__":
    fname = "/Users/gertjan/Documents/energie rekening/energie_tolakkerweg.numbers"
    keys = ["date", "consume", "supply"]
    subkeys = ["low", "high"]
    energy = Energy(fname)
    for row in energy.doc.iter_rows(min_row=1, min_col=0, max_row=energy.doc.num_rows-1,
                                   max_col=5, values_only=True):
        formatted_row = [int(i) if isinstance(i,float) else i for i in row]
        consume = dict(zip(subkeys, formatted_row[1:3]))
        supply = dict(zip(subkeys, formatted_row[3:5]))
        energy = dict(zip(keys, [f"{row[0]:%Y-%m-%d}", consume, supply]))
        print(energy)