from numpy import random as rnd


class Player:

    def __init__(self):
        mu = 0
        char = []
        self.lefty: bool = (rnd.random() < 0.15)
        while not (0 < mu < 5):
            mu = rnd.pareto(2-int(self.lefty)*0.1)
        sigma = mu/5
        while len(char) != 3:
            apnd = rnd.uniform(mu-sigma, mu+sigma)
            if 0 < apnd < 5:
                char.append(apnd)

        self.service: float = char[0]
        self.defence: float = char[1]
        self.offence: float = char[2]
        self.char = {
            'srv': self.service,
            'def': self.defence,
            'off': self.offence
        }
        self.tilt: float = 0

    def __repr__(self):
        return f'{self.lefty} Player service-{round(self.service,2)} def-{round(self.defence,2)} off-{round(self.offence,2)}'

    def __iter__(self):
        yield self

    def get_char(self):
        return self.char

    def mood(self, change):
        if self.tilt - change > 1:
            self.tilt = 1
            tilt_factor = 1 - self.tilt/3
            self.char = {
                'srv': self.service * tilt_factor,
                'def': self.defence * tilt_factor,
                'off': self.offence * tilt_factor
            }
        elif self.tilt - change < 0:
            self.tilt = 0
            tilt_factor = 1 - self.tilt/3
            self.char = {
                'srv': self.service * tilt_factor,
                'def': self.defence * tilt_factor,
                'off': self.offence * tilt_factor
            }
        else:
            self.tilt -= change
            tilt_factor = 1 - self.tilt/3
            self.char = {
                'srv': self.service * tilt_factor,
                'def': self.defence * tilt_factor,
                'off': self.offence * tilt_factor
            }


def Game(p1, p2):
    players = {p1, p2}
    turn = rnd.choice(list(players))
    recieve = (players - set(turn)).pop()
    n = 0
    score = {
        p1: 0,
        p2: 0
    }

    while max(score.values()) < 11:

        for i in range(2):
            print(score, n)
            winner = 0
            n = 0
            char = {
                p1: p1.get_char(),
                p2: p2.get_char()
            }

            P_srv = 0.9 - 0.15*char[turn]['srv'] + 0.05 * char[recieve]['def']
            n += 1
            if rnd.random() < (1 - P_srv):
                winner = turn
                winner.mood(0.03)
                (players - set(winner)).pop().mood(-0.03)

            while winner == 0:
                if not n % 2:
                    hit = turn
                else:
                    hit = recieve
                rec = (players - set(hit)).pop()

                off_diff = char[hit]['off'] - char[rec]['off']
                def_diff = char[hit]['def'] - char[rec]['def']
                P = 0.5 + 0.2*def_diff + 0.1*off_diff + rnd.normal(0, 0.05)
                n += 1
                if rnd.random() < P:
                    winner = hit
                    winner.mood(n*0.01)
                    (players - set(winner)).pop().mood(-n*0.01)

            score[winner] += 1
            recieve = turn
            turn = (players - set(turn)).pop()

    return p1 if score[p1] == 11 else p2


if __name__ == '__main__':
    p1 = Player()
    p2 = Player()
    Game(p1, p2)
