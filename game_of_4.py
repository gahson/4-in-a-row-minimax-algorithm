# -*- coding: utf-8 -*-

end = None


from time import sleep
from random import choice

plansza = [[' ' for _ in range(7)] for _ in range(6)]


def rysuj(s):
    '''rysuje plansze w trybie tekstowym'''

    for i in range(1, 8): print(i, end=' ')
    print()
    print('-' * 14)

    for w in range(6):
        for k in range(7):
            if s[w][k] == ' ':
                print('.', end=' ')
            else:
                print(s[w][k], end=' ')
        print()
    end
    print()


end


def moj_ruch(s):
    '''pozwala wykonac ruch w grze przez wprowadzenie numeru kolumny 1-7
       zwraca stan planszy po wykonaniu ruchu
       My gramy krzyzykiem "X" '''
    while True:
        try:
            k = int(input('>>')) - 1
            if s[0][k] == ' ': break
        except:
            pass
        end
    end
    for w in range(5, -1, -1):
        if s[w][k] == ' ':
            s[w][k] = 'X'
            return
        end
    end


end
def min_max(s,player,depth=5):
    moves=possible_columns(s)
    if player :
        best = [choice(moves),float('-inf')]
        mark='X'
    else:
        best =  [choice(moves),float('inf')]
        mark='O'
    res=czy_koniec(s)
    if depth == 0 or res is not None:
        if res=='X':
            return [choice(moves),1]
        elif res=='O':
            return [choice(moves),-1]
        else:
            return [choice(moves),0]

    for mov in moves:
        if s[0][mov]!=' ':
            continue
        to_rem=None
        for w in range(5, -1, -1):
            if s[w][mov] == ' ':
                s[w][mov] = mark
                to_rem=w
                break

        score = min_max(s.copy(),not player, depth - 1)
        score[0]=mov
        s[to_rem][mov]=' '


        if player:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score

    return best

def possible_columns(s):
    pos_mov=[]
    for move in range(7):
        if s[0][move]==' ':
            pos_mov.append(move)
    return pos_mov

def ruch_komp(s):
    '''wykonuje ruch komputera poprzez wylosowanie kolumny
       zwraca stan planszy po wykonaniu ruchu
       Komputer gra kolkiem "O" '''


    k,_=min_max(s.copy(),False)
    for w in range(5, -1, -1):
        if s[w][k] == ' ':
            s[w][k] = 'O'
            return
    end


end


def czy_koniec(s):
    '''sprawdza czy natapil koniec gry. Zwraca:
      'X' lub 'O' gdy jedna ze stron wyrala
      '?' gdy zapelniono plansze i nikt nie wygral
      None gdy gre nalezy kontynuowac'''

    # czy s� 4 w poziomie
    for w in range(6):
        for k in range(4):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w][k + i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s� 4 w pionie
    for w in range(3):
        for k in range(7):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s� 4 uko�nie \
    for w in range(3):
        for k in range(4):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k + i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s� 4 uko�nie /
    for w in range(3):
        for k in range(3, 7):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k - i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy plansza jest pelna
    for k in range(7):
        if s[0][k] == ' ': break
    else:
        return '?'
    end

    return None


end

rysuj(plansza)
b=int(input("czy chcesz rozpocząć 1-tak,0-nie\n>>"))
if b==0:
    ruch_komp(plansza)
    rysuj(plansza)
elif b!=1:
    raise ValueError("Invalid input: please enter 1 for 'tak' or 0 for 'nie'")




while True:

    moj_ruch(plansza)
    rysuj(plansza)

    k = czy_koniec(plansza)
    if k == '?':
        print('Remis')
        break
    elif k != None:
        print(f'Wygral {k}')
        break
    end

    ruch_komp(plansza)
    sleep(0.5)
    rysuj(plansza)

    k = czy_koniec(plansza)
    if k == '?':
        print('Remis')
        break
    elif k != None:
        print(f'Wygral {k}')
        break
    end

end