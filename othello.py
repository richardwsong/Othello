import random
import sys
import time

sys.setrecursionlimit(1000000)
arr = [-1, 1, -10, 10, -9, 9, -11, 11]
corners = {11, 18, 81, 88}
#corner_mapping = {11: (12, 21), 18: (17, 27), 81: (71, 82), 88: (87, 78)}
corner_mapping = {12:11, 21:11, 22:11, 17:18, 27: 18, 28: 18, 71:81, 72:81, 82: 81, 87:88, 77: 88, 78:88}
edges = {13, 14, 15, 16, 31, 41, 51, 61, 38, 48, 58, 68, 83, 84, 85, 86}
edges_mapping = {13: (11, 18), 14:(11,18), 15:(11,18), 16:(11, 18), 31:(11, 81), 41:(11, 81), 51:(11, 81), 61: (11, 81),
                 38: (18, 88), 48: (18, 88), 58: (18, 88), 68:(18, 88), 83:(81, 88), 84:(81, 88), 85: (81, 88),
                 86: (81, 88)}
true_edges = {12, 13, 14, 15, 16, 17, 21, 31, 41, 51, 61, 71, 28, 38, 48, 58, 68, 78, 82, 83, 84, 85, 86, 87}
next_to_corner = {12, 21, 22, 17, 27, 28, 71, 72, 82, 87, 77, 78}
next_to_edge = {23, 24, 25, 26, 32, 42, 52, 62, 37, 47, 57, 67, 73, 74, 75, 76}
middle = {33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66}

#board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"


def comparator(x):
    xval= -1
    if x[0] in corners: xval = 0
    elif x[0] in edges: xval = 1
    elif x[0] in middle: xval = 2
    elif x[0] in next_to_edge: xval = 3
    else: xval = 4

    return xval


def possibleMoves(board, you, opponent):
    ret = []
    index = -1
    for x in board:
        index += 1
        if x != ".":
            continue
        moves_list = []
        for y in arr:
            if possibleMovesHelper(index, y, board, you, opponent):
                moves_list.append(y)
        if len(moves_list) != 0:
            ret.append((index, moves_list))
    return sorted(ret, key=comparator)
    #return ret

def raw_possible_Moves(board, you, opponent):
    ret = []
    index = -1
    for x in board:
        index += 1
        if x != ".":
            continue
        for y in arr:
            if possibleMovesHelper(index, y, board, you, opponent):
                ret.append((index, y))
                break
    return len(ret)

def possibleMovesHelper(index, move, board, you, opponent):
    if board[index+move] != opponent:
        return False
    temp = index
    while True:
        temp += move
        if board[temp] == you:
            return True
        if board[temp] == ".":
            return False
        if board[temp] == "?":
            return False


def move(board, token, valid):
    index = valid[0]
    poss_dir = valid[1]
    board = board[0:index] + token + board[index+1:]
    current_player = "@" if token == "o" else "o"

    for dir in poss_dir:
        temp = index + dir
        while board[temp] == current_player:
            board = board[0:temp] + token + board[temp + 1:]
            temp += dir
    return board


def currentScore(board, token):
    return len([i for i, pos in enumerate(board) if pos == token])


def printboard(board):
    for x in range(0, len(board), 10):
        print(board[x:x+10])


def isGameOver(board):
    return currentScore(board, ".") == 0


def genMoves(board, val, you, opponent):
    ret = []
    temp = possibleMoves(board, you, opponent)
    for x in temp:
        if val == x[0]:
            return x[1]

# count = 0
# moves = []
# pass_moves = 0
# while not isGameOver(board) and pass_moves < 2:
#     printboard(board)
#     print("@:", currentScore(board, "@"))
#     print("o:", currentScore(board, "o"))
#
#     validMoves = set()
#     cur = ""
#     if count%2 == 0:
#         ret = possibleMoves(board, "@", "o")
#         cur = "@"
#     else:
#         ret = possibleMoves(board, "o", "@")
#         cur = "o"
#     count += 1
#     if len(ret) > 0:
#         print("Valid Moves:", end=" ")
#         for x in ret:
#             if x[0] not in validMoves:
#                 print(x[0], end=" ")
#                 validMoves.add(x[0])
#         print()
#         rand = random.randint(0, len(validMoves)-1)
#         print("Move at", ret[rand][0], "was chosen.")
#         moves.append(ret[rand][0])
#         for x in ret:
#             if x[0] == ret[rand][0]:
#                 board = move(board, cur, x)
#         pass_moves = 0
#     else:
#         print("Valid Moves: None")
#         print("Pass")
#         moves.append(-1)
#         pass_moves += 1
# printboard(board)
# print()
#
# black_score = currentScore(board, "@")
# white_score = currentScore(board, "o")
# total_pieces = 64 - currentScore(board, ".")
# print("@:", currentScore(board, "@"))
# print("o:", currentScore(board, "o"))
# print("@:", "%0.2f"%(black_score/total_pieces * 100), end="")
# print("%")
# print("o:", "%0.2f"%(white_score/total_pieces * 100), end="")
# print("%")
# print(moves)


def number_of_components_taken(board, token, type):
    res = 0
    for c in type:
        if board[c] == token:
            res += 1
    return res
#
#
# def vulnerability(board, token, total_moves):
#     # 3 Cases: Completely Safe, Semi-Safe, Unsafe
#
#     # Case 1: Completely Safe
#     corners_taken = []
#     for a in corners:
#         if board[a] == token: corners_taken.append(a)
#
#     safe = len(corners_taken)
#     for c in corners_taken:
#         for nc in corner_mapping[c]:
#             if board[nc] == token:
#                 safe += 1
#                 dir = nc - c
#                 temp = nc + dir
#                 while board[temp] == token:
#                     safe += 1
#                     temp += dir

    # Case 2 and 3: Semi-Safe and Unsafe, has weighting in the mid-game.
    # semi = set()
    # unsafe = 0
    # semi_safe = 0
    # if 20 <= total_moves <= 45:
    #     for a in true_edges:
    #         if a < 20:
    #             dir = 10
    #         elif (a-1)%10:
    #             dir = 1
    #         elif (a+2)% 10:
    #             dir = -1
    #         else:
    #             dir = -10
    #         temp = a + dir
    #         while board[temp] == token:
    #             semi.add(board[temp])
    #             temp += dir
    #     semi_safe = len(semi)
    #     unsafe = currentScore(board, token) - semi_safe - safe
    return safe

def num_full(board, token):
    # Counts the number of full rows and columns, to be considered important late game
    column_start = [1, 2, 3, 4, 5, 6, 7, 8]
    row_start = [10, 20, 30, 40, 50, 60, 70, 80]
    score = 0
    for x in column_start:
        bad = False
        temp = x
        counter = 1
        for z in range(0, 10):
            if board[temp] == "?" or board[temp] == token:
                temp += 10
                counter+=1
            elif board[temp] != token:
                break
        if counter >= 6:
            score+=1

    for x in row_start:
        bad = False
        temp = x
        counter = 1
        for z in range(0, 10):
            if board[temp] == "?" or board[temp] == token:
                temp += 1
                counter+=1
            elif board[temp] != token:
                break
        if counter>=6:
            score+=1
    return score


def edgescalc(board, token, totalmoves):
    # ADVANCED - More in Writeup
    score = 0
    for e in edges:
        if totalmoves < 20:
            if board[edges_mapping[e][0]] == token or board[edges_mapping[e][0]] == token:
                score += 500000
            else:
                score += 30000
        elif totalmoves < 40:
            if board[edges_mapping[e][0]] == token or board[edges_mapping[e][0]] == token:
                score += 900000
            else:
                score += 55000
        else:
            if board[edges_mapping[e][0]] == token or board[edges_mapping[e][0]] == token:
                score += 1000000
            else:
                score += 75000
    return score


def nexttocornercalc(board, token):
    ret = 0
    for n in next_to_corner:
        if board[corner_mapping[n]] != token:
            ret+=1
    return ret


def eval(board, you, opponent):

    score = 0

    # # Case 1: Number of Tokens
    you_tokens = currentScore(board, you)
    opp_tokens = currentScore(board, opponent)

    # Q2 The number of tokeens matters much more when the total tokens is > 60 compared to any other total tokens value.

    if you_tokens + opp_tokens > 60:
        score += 0 if you_tokens + opp_tokens == 0 else 10000000 * (you_tokens - opp_tokens)
    elif you_tokens + opp_tokens > 55:
        score += 0 if you_tokens + opp_tokens == 0 else 200000 * (you_tokens - opp_tokens)

    # Case 2: Number of Possible Moves
    poss = possibleMoves(board, you, opponent)
    you_moves = len(poss)
    opp_moves = 100
    for a in poss:
        opp_moves = min(opp_moves, len(possibleMoves(move(board, you, a), opponent, you)))

    if you_moves == 0 and opp_moves == 0:
        if you_moves > opp_moves:
            return 10000000
        else:
            return -10000000

    total_moves = you_moves + opp_moves

    if total_moves <= 20:
        score += 300000 * (you_moves-opp_moves)
    if you_tokens + opp_tokens <= 40:
        score += 300000 * (you_moves-opp_moves)
    elif you_tokens + opp_tokens <= 60:
        score += 400000 * (you_moves-opp_moves)

    # Case 3: Number of Corners Captured, Weight of 100
    you_corners = number_of_components_taken(board, you, corners)
    opp_corners = number_of_components_taken(board, opponent, corners)
    score += 15000000 * (you_corners - opp_corners)

    # Case 4: Number of Edges Captured

    you_edges = edgescalc(board, you, total_moves)
    opp_edges = edgescalc(board, opponent, total_moves)
    score += (you_edges - opp_edges)



    # Case 5: Number of Next to Corners Captured

    you_adjc = nexttocornercalc(board, you)
    opp_adjc = nexttocornercalc(board, opponent)
    score -= 7000000*(you_adjc-opp_adjc)


    # Case 6 : Parity
    if total_moves > 57:
        if (64 - total_moves)%2 == 0:
            score -= 300000
        else:
            score += 300000
    elif total_moves > 50:
        if (64 - total_moves)%2 == 0:
            score -= 100000
        else:
            score += 100000

    return score


# Q1 - Alpha Beta. I have a minimum and a maximum function, where max calls min and min calls max; this also assumes
# that maximum is the computer. When maximum realizes that the score returned is higher than the beta, it produces a
#  cuttoff, likewise, when minimum realizes that the score returned is lower than the alpha, it cutsoff.

def maximum(board, maxplayer, minplayer, depth, target_depth, alpha, beta, initial):
    if depth == target_depth or isGameOver(board):
        return eval(board, maxplayer, minplayer)
    v = -1 * sys.maxsize
    ret = -1
    arr = possibleMoves(board, maxplayer, minplayer)
    if len(arr) == 0:
        v = minimum(board, maxplayer, minplayer, depth+1, target_depth, alpha, beta)
    for a in arr:
        nv = max(v, minimum(move(board, maxplayer, a), maxplayer, minplayer, depth+1, target_depth, alpha, beta))
        if initial and nv > v:
            ret = a[0]
        if nv>v:
            v = nv
        if v >= beta and not initial:
            return v
        alpha = max(alpha, v)
    if initial:
        return ret
    return v


def minimum(board, maxplayer, minplayer, depth, target_depth, alpha, beta):
    if depth == target_depth or isGameOver(board):
        return eval(board, minplayer, maxplayer)
    v = sys.maxsize
    arr = possibleMoves(board, minplayer, maxplayer)
    if len(arr) == 0:
        v = maximum(board, maxplayer, minplayer, depth+1, target_depth, alpha, beta, False)
    for a in arr:
        v = min(v, maximum(move(board, minplayer, a), maxplayer, minplayer, depth+1, target_depth, alpha, beta, False))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


board = sys.argv[1]
maxplayer = sys.argv[2]
if maxplayer == "@":
    minplayer = "o"
else:
    minplayer = "@"


def play(depth):
    counter = 1
    val = -1
    while counter < depth:
        val = maximum(board, maxplayer, minplayer, 0, counter, -1 * sys.maxsize, sys.maxsize, True)
        counter+=2
    return val
# board = "??????????" \
#         "?........?" \
#         "?........?" \
#         "?..oo@...?" \
#         "?..oo@o..?" \
#         "?..o@@oo.?" \
#         "?.o@@@@..?" \
#         "?...o@@..?" \
#         "?..o.o@..?" \
#         "??????????"


def negascout(board, depth, alpha, beta, you, opp, initial):
    # ADVANCED - Explained in Write Up
    if depth == 0 or isGameOver(board):
        return eval(board, you, opp)
    counter = 0
    ret = 0
    arr = possibleMoves(board, you, opp)
    a = alpha
    b = beta
    best_val = -sys.maxsize
    if len(arr) == 0:
        a = -negascout(board, depth-1, alpha, beta, opp, you, False)
    for child in arr:
        valid = move(board, you, child)
        score = -negascout(valid, depth-1, -b, -a, opp, you, False)
        counter+=1
        if score > a and score < beta and counter > 1 and depth > 1:
            a = -negascout(valid, depth-1, -beta, -score, opp, you, False)
        a = max(a, score)
        if initial and a > best_val:
            ret = child[0]
            best_val = a
        if a >= beta:
            return a
        b = a + 1
    if initial:
        return ret
    return a


def makemove(board, depth, you, opp):
    temp = negascout(board, depth, -sys.maxsize, sys.maxsize, you, opp, True)
    return temp


# turn = "@"
# board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
# maxplayer = "@"
# minplayer = "o"
# turn = "o"

counter = 2
while True:
    print(makemove(board, counter, maxplayer, minplayer))
    counter += 2

