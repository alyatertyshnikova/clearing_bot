class TeamExpenses:
    def __init__(self, user_id: str):
        self._user_id = user_id
        self._values = {}

    def write_names(self, message: str):
        """
        :param message: Write names of team
        :return:
        """
        names = message.split()[1:]
        for name in names:
            self._values.update({name: {}})

    def write_payment(self, message: str):
        """
        :param message: Write payment to the team expenses file
        :return:
        """
        _, payer, price, *debtors = message.split()
        is_debtor_not_in_the_team = any(debtor not in self._values.keys() for debtor in debtors)
        if payer not in self._values.keys() or is_debtor_not_in_the_team:
            not_team_members = ({payer} | set(debtors)) - self._values.keys()
            raise ValueError(f"Incorrect names: {not_team_members} is not in the team")

        debt = round(float(price)/len(debtors), 2)
        for debtor in debtors:
            if debtor == payer:
                continue
            payer_debt = self._values[debtor].get(payer, 0)
            remain = payer_debt - debt
            if remain < 0:
                latest_debtor_debt = self._values[payer].get(debtor, 0)
                self._values[payer][debtor] = latest_debtor_debt + abs(remain)
                self._values[debtor][payer] = 0
            else:
                self._values[debtor][payer] = remain

    def get_clearing_result(self) -> str:
        """
        :return: Clearing result
        """
        result = ""
        for payer, debts in self._values.items():
            result += f"To {payer}\n {debts}\n"
        return result
