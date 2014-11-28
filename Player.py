__author__ = 'user'



class Player:
    lines = []
    current_turn = -1

    def __init__(self, name):
        lines = self.open_file(name)
        for line in lines:
            temp_lines = line.split(' ')
            for tl in temp_lines:
                self.lines.append(tl)

    def open_file(self, name):
        return open(name).readlines()

    def get_turn(self):
        acceptable_list = "abcdefgh123456780"
        turn_string = ''
        for letter in self.lines[self.current_turn]:
            if letter in acceptable_list:
                turn_string += letter
        if turn_string[0:2] == '00':
            if len(turn_string) == 3:
                turn_string += '0'
            else:
                turn_string += '01'
            if self.current_turn % 2 != 0:
                turn_string[0:2] = '01'

        return turn_string[0:2], turn_string[2:4], self.lines[self.current_turn]

    def get_next_turn(self):
        self.current_turn += 1
        return self.get_turn()

    def get_prev_turn(self):
        if self.current_turn != -1:
            self.current_turn -= 1
            return self.get_turn()
        else:
            return self.get_turn()

    def get_game(self):
        frm = []
        to = []
        turn = []
        for i in range(len(self.lines)):
            a, b, c = self.get_next_turn()
            frm.append(a)
            to.append(b)
            turn.append(c)
        return frm, to, turn

