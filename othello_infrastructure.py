import random
import sys
import time

sys.setrecursionlimit(1000000)
arr = [-1, 1, -10, 10, -9, 9, -11, 11]
corners = {11, 18, 81, 88}
corner_mapping = {11: (12, 21), 18: (17, 27), 81: (71, 82), 88: (87, 78)}
edges = {13, 14, 15, 16, 31, 41, 51, 61, 38, 48, 58, 68, 83, 84, 85, 86}
true_edges = {12, 13, 14, 15, 16, 17, 21, 31, 41, 51, 61, 71, 28, 38, 48, 58, 68, 78, 82, 83, 84, 85, 86, 87}
next_to_corner = {12, 21, 22, 17, 27, 28, 71, 72, 82, 87, 77, 78}
next_to_edge = {23, 24, 25, 26, 32, 42, 52, 62, 37, 47, 57, 67, 73, 74, 75, 76}
middle = {33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66}

#board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"


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
    return ret


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


def vulnerability(board, token, total_moves):
    # 3 Cases: Completely Safe, Semi-Safe, Unsafe

    # Case 1: Completely Safe
    corners_taken = []
    for a in corners:
        if board[a] == token: corners_taken.append(a)

    safe = len(corners_taken)
    for c in corners_taken:
        for nc in corner_mapping[c]:
            if board[nc] == token:
                safe += 1
                dir = nc - c
                temp = nc + dir
                while board[temp] == token:
                    safe += 1
                    temp += dir

    # Case 2 and 3: Semi-Safe and Unsafe, has weighting in the mid-game.
    semi = set()
    unsafe = 0
    semi_safe = 0
    if 20 <= total_moves <= 45:
        for a in true_edges:
            if a < 20:
                dir = 10
            elif (a-1)%10:
                dir = 1
            elif (a+2)% 10:
                dir = -1
            else:
                dir = -10
            temp = a + dir
            while board[temp] == token:
                semi.add(board[temp])
                temp += dir
        semi_safe = len(semi)
        unsafe = currentScore(board, token) - semi_safe - safe
    return 2*safe + semi_safe + -1*safe


def eval(board, you, opponent):
    # Eval function computes number of tokens on both sides, the number of possible moves from both sides, the number of
    # corners/edges captured from both sides, and the number of tokens from both sides that are easily flanked

    score = 0

    # Case 1: Number of Tokens, Weight of 30
    you_tokens = currentScore(board, you)
    opp_tokens = currentScore(board, opponent)
    if you_tokens + opp_tokens > 50:
        score += 0 if you_tokens + opp_tokens == 0 else 100 * (you_tokens - opp_tokens)/(you_tokens + opp_tokens)

    # Case 2: Number of Possible Moves, Weight of 90
    you_moves = raw_possible_Moves(board, you, opponent)
    opp_moves = raw_possible_Moves(board, opponent, you)
    total_moves = you_moves + opp_moves
    if you_tokens + opp_tokens > 30:
        score += 0 if you_moves + opp_moves == 0 else 250 * (you_moves - opp_moves) / (you_moves + opp_moves)

    # Case 3: Number of Corners Captured, Weight of 100
    you_corners = number_of_components_taken(board, you, corners)
    opp_corners = number_of_components_taken(board, opponent, corners)
    score += 0 if you_corners + opp_corners == 0 else 430 * (you_corners - opp_corners) / (you_corners + opp_corners)

    # Case 4: Number of Edges Captured, Weight of 50
    you_edges = number_of_components_taken(board, you, edges)
    opp_edges = number_of_components_taken(board, opponent, edges)
    score += 0 if you_edges + opp_edges == 0 else 80 * (you_edges - opp_edges) / (you_edges + opp_edges)

    # Case 5: Number of Next to Corners Captured, Weight of 80
    if total_moves < 60:
        you_adjc = number_of_components_taken(board, you, next_to_corner)
        opp_adjc = number_of_components_taken(board, opponent, next_to_corner)
        score -= 0 if you_adjc + opp_adjc == 0 else 430 * (you_adjc - opp_adjc) / (you_adjc + opp_adjc)

    # Case 6: Number of Next to Edges Captured, Weight of 40
    if total_moves < 60:
        you_adje = number_of_components_taken(board, you, next_to_edge)
        opp_adje = number_of_components_taken(board, opponent, next_to_edge)
        score -= 0 if you_adje + opp_adje == 0 else 60 * (you_adje - opp_adje) / (you_adje + opp_adje)

    # Case 7: Vulnerability
    # you_vul = vulnerability(board, you, total_moves)
    # opp_vul = vulnerability(board, opponent, total_moves)
    # if you_vul + opp_vul != 0:
    #     if total_moves > 50:
    #         score += 500*((you_vul - opp_vul)/(you_vul + opp_vul))
    #     elif total_moves > 20:
    #         score += 200*((you_vul - opp_vul)/(you_vul + opp_vul))

    return score



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

#

# board = "??????????" \
#         "?..@@@@@@?" \
#         "?..o@@o..?" \
#         "?..o@ooo.?" \
#         "?.oooo...?" \
#         "?..ooo...?" \
#         "?........?" \
#         "?........?" \
#         "?........?" \
#         "??????????"
# board = "??????????" \
#         "?@@@@@@@@?" \
#         "?@@@@@@@@?" \
#         "?@@@@@@@@?" \
#         "?@@@@@@@@?" \
#         "?@@@o@@@@?" \
#         "?@@@@@@@@?" \
#         "?@@@@@@@@?" \
#         "?oooo..@@?" \
#         "??????????"

maxplayer = "@"
if maxplayer == "@":
    minplayer = "o"
else:
    minplayer = "@"


def play(depth):
    counter = 1
    val = -1
    while counter < depth:
        val = maximum(board, maxplayer, minplayer, 0, counter, -1 * sys.maxsize, sys.maxsize, True)
        counter+=1
    return val


f1 = open("results.txt", "w")
# f1.write(str(5))
for t in range(0, 1):
    board = "??????????" \
            "?........?" \
            "?........?" \
            "?........?" \
            "?...o@...?" \
            "?...@o...?" \
            "?........?" \
            "?........?" \
            "?........?" \
            "??????????"
    skip = 0
    while not isGameOver(board) and skip != 2:
        skip = 0
        new_moves = possibleMoves(board, minplayer, maxplayer)

        if len(new_moves) == 0:
            print("Skipped")
            printboard(board)
            skip += 1


        choices = possibleMoves(board, minplayer, maxplayer)
        print(choices)
        # pl = int(input("Your move:"))
        pl = choices[random.randint(0, len(choices)-1)]
        # poss = genMoves(board, pl, minplayer, maxplayer)
        board = move(board, minplayer, pl)
        printboard(board)
        print()

        val = play(7)
        print(val)
        if val == -1:
            print("Computer Skipped")
            skip+=1
            printboard(board)
            if skip == 2:
                break
        else:
            skip = 0
            poss = genMoves(board, val, maxplayer, minplayer)
            board = move(board, maxplayer, (val, poss))
            printboard(board)



    black_score = currentScore(board, "@")
    white_score = currentScore(board, "o")
    # black_score = 48
    # white_score = 12
    f1.write(str(black_score)+"\n")
    f1.write(str(white_score)+ "\n")
    f1.write(str(black_score/(black_score+white_score)*100)+"%\n")
    f1.write("\n")

f1.close()
