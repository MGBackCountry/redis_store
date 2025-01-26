from enum import Enum
from numbers_parser import Document


class Headers(Enum):
    WORKSHEET = "/Users/gertjan/Documents/energie rekening/energie_tolakkerweg.numbers"
    PRIMARYKEYS = ("date", "consume", "supply")
    SECONDARYKEYS = ("low", "high")


class EnergyProvision:

    def __init__(self, worksheet):
        self._line = None
        self.worksheet = worksheet

    @property
    def worksheet(self):
        return self._worksheet

    @worksheet.setter
    def worksheet(self, worksheet):
        self._worksheet = Document(worksheet).sheets[0].tables[0]

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line_number: int):
        formatted_line = [int(i) if isinstance(i, float) else i
                          for i in self.worksheet.rows(values_only=True)[line_number]]
        consume = dict(zip(Headers.SECONDARYKEYS.value, formatted_line[1:3]))
        supply = dict(zip(Headers.SECONDARYKEYS.value, formatted_line[3:5]))
        self._line = dict(zip(Headers.PRIMARYKEYS.value,
                          [f"{formatted_line[0]:%Y-%m-%d}", consume, supply]))

if __name__ == "__main__":
    energy_provision = EnergyProvision(Headers.WORKSHEET.value)
    energy_provision.line = energy_provision.worksheet.num_rows - 1
    print(energy_provision.line)
    '''
    for row in energy_provision.worksheet.iter_rows(min_row=1, min_col=0,
                                                    max_row=energy_provision.worksheet.num_rows - 1,
                                                    max_col=5, values_only=True):
        formatted_row = [int(i) if isinstance(i, float) else i for i in row]
        consume = dict(zip(Headers.SECONDARYKEYS.value, formatted_row[1:3]))
        supply = dict(zip(Headers.SECONDARYKEYS.value, formatted_row[3:5]))
        energy_provision = dict(zip(Headers.PRIMARYKEYS.value, [f"{row[0]:%Y-%m-%d}", consume, supply]))
        print(energy_provision)
    '''
