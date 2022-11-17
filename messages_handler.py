class TeamExpenses:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.team_expenses = {}

    def write_names(self, message: str):
        """
        :param message: Write names of team
        :return:
        """
        names = message.split()[1:]
        for name in names:
            self.team_expenses.update({name: {}})

    def write_payment(self, message: str):
        """
        :param message: Write payment to the team expenses file
        :return:
        """
        _, payer, price, *debtors = message.split()
        debt = round(int(price)/len(debtors), 2)
        for debtor in debtors:
            if debtor != payer:
                payer_debt = self.team_expenses[debtor].get(payer, 0)
                remain = payer_debt - debt
                if remain < 0:
                    latest_debtor_debt = self.team_expenses[payer].get(debtor, 0)
                    self.team_expenses[payer][debtor] = latest_debtor_debt + abs(remain)
                    self.team_expenses[debtor][payer] = 0
                else:
                    self.team_expenses[debtor][payer] = remain
# with open("team_expenses.yaml", "w") as f:
#     yaml.dump(team_expenses, f)
    # with open("team_expenses.yaml", "r") as f:
    #     team_expenses = yaml.safe_load(f)
    #     for debtor in debtors:
    #         if debtor != payer:
    #             payer_debt = team_expenses[debtor].get(payer, 0)
    #             remain = payer_debt - debt
    #             if remain < 0:
    #                 latest_debtor_debt = team_expenses[payer].get(debtor, 0)
    #                 team_expenses[payer][debtor] = latest_debtor_debt + abs(remain)
    #                 team_expenses[debtor][payer] = 0
    #             else:
    #                 team_expenses[debtor][payer] = remain
    # with open("team_expenses.yaml", "w") as f:
    #     yaml.dump(team_expenses, f)

    def get_clearing_result(self) -> str:
        """
        :return: Clearing result
        """
        result = ""
        for payer, debts in self.team_expenses.items():
            result += f"To {payer}\n {debts}\n"
        return result
