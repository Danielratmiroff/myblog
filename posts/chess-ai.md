[category]: <> (side projects)
[date]: <> (2022/12/05)
[title]: <> (Chess AI)
[color]: <> (green)

## Overview

![AI](https://img.shields.io/badge/AI-100-purple)
![smartass](https://img.shields.io/badge/smartass-69-green)

I built an AI that plays chess and it kicked my ass

[Play ](https://chess-ai-danielratmiroff.vercel.app/) ![Visit App](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

[Source code](https://github.com/Danielratmiroff/chess-ai) ![Github](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

**What does it do?**

- Plays "good" moves
- Beats other players
- Speaks when beating other players

## How?

You might be wondering, how one creates an Chess AI? or how bad is Daniel at Chess exactly?

For those two questions, two short answers:

- It's easy
- Very bad

### Let's elaborate on the how

First of all, we need an GUI. I chose Javascript since there are many chess libraries available to choose from. That's very convenient since I didn't want to re-invent the wheel.

I used:

- Board's UI: [cm-chessboard](https://www.npmjs.com/package/cm-chessboard)
- Move validation and chess functionality: [chess.js](https://github.com/jhlywa/chess.js/blob/master/README.md)

Once we got the board and input validation going, things start to get interesting...

## AI

> "AI without data, go prrrrrrrrrrrrr."

> -- Anounymus Philosopher

We don't want an AI that just plays random moves, so we need to give it data to evaluate which moves are better.

First, each piece needs a value:

- Pawn: 100
- Knight: 280
- Bishop: 320
- Rook: 479
- Queen: 929
- King: 60,000

Each piece's position in the board needs a value too

```javascript
// PAWN
p: [
	[100, 100, 100, 100, 105, 100, 100, 100],
	[78, 83, 86, 73, 102, 82, 85, 90],
	[7, 29, 21, 44, 40, 31, 44, 7],
	[-17, 16, -2, 15, 14, 0, 15, -13],
	[-26, 3, 10, 9, 6, 1, 0, -23],
	[-22, 9, 5, -11, -10, -2, 3, -19],
	[-31, 8, -7, -37, -36, -14, 3, -31],
	[0, 0, 0, 0, 0, 0, 0, 0]
]
...
```

_Get the whole table scores here: [Board scores](https://github.com/Danielratmiroff/chess-ai/blob/master/src/lib/data/table-scores.ts)_

I'm not a chess expert. I took these values from the incredible chess engine [Sunfish](https://github.com/thomasahle/sunfish/blob/master/sunfish.py)

## Evaluate

Chess is a **zero-sum game**. _(One player's advantage is equivalent to the other player's loss)_. There are various existing algorithms that solve 'zero-sum' problems. Like: Negamax or Minimax

No matter the algorithm we chose, we need an **evaluation function** that calculates the board's positions and returns a score.

We will use this score to let the AI know which positions are good or bad.

```
// Idea behind evaluation function
function evaluateBoard(game: Chess) {
  const board = game.board();
  var totalEvaluation = 0;
  for (var row = 0; row < 8; row++) {
    for (var col = 0; col < 8; col++) {
      totalEvaluation += getPieceValue(board[row][col], row, col);
    }
  }
  return totalEvaluation;
}
```

_Get the whole function: [Evaluation function](https://github.com/Danielratmiroff/chess-ai/blob/master/src/lib/components/evaluateBoard.ts)_

## Think AI, think!

I chose to implement the **Minimax algorithm** with **Alpha-beta prunning**. What do those fancy words mean?

&nbsp;

**Minimax algorithm:**

> A **minimax algorithm**[[5]](https://en.wikipedia.org/wiki/Minimax#cite_note-5) is a recursive [algorithm](https://en.wikipedia.org/wiki/Algorithm "Algorithm") for choosing the next move in an n-player [game](https://en.wikipedia.org/wiki/Game_theory "Game theory"), usually a two-player game. A value is associated with each position or state of the game. This value is computed by means of a [position evaluation function](https://en.wikipedia.org/wiki/Evaluation_function "Evaluation function") and it indicates how good it would be for a player to reach that position. The player then makes the move that maximizes the minimum value of the position resulting from the opponent's possible following moves.
>
> -- Wikipedia

&nbsp;

**Alpha-prunning:**

> **Alpha–beta pruning** is a [search algorithm](https://en.wikipedia.org/wiki/Search_algorithm "Search algorithm") that seeks to decrease the number of nodes that are evaluated by the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves "Minimax") in its [search tree](https://en.wikipedia.org/wiki/Game_tree "Game tree").
> -- Wikipedia

&nbsp;

_Wow, that is awesome! but I didn't understand a single word!_

&nbsp;

I recommend watching John Levine's awesome video explaining how the Minimax algorithm with Alpha Prunning works: [Minimax Explanation](https://www.youtube.com/watch?v=zp3VMe0Jpf8&ab_channel=JohnLevine)

&nbsp;

**In simple words**: Minimax recursevily evaluates the possible moves and alpha-prunning makes it go fast\*

```typescript
/**
Alpha = best value for MAX
Beta = best value for MIN
Depth = depth of search
maximizingPlayer = AI
**/
type AlphaBetaReturn = [bestScore: number, bestMove: Move | null];
type AlphaBeta = {
  game: Chess;
  alpha: number;
  beta: number;
  depth: number;
  maximizingPlayer: boolean;
};

function minimax({
  game,
  alpha,
  beta,
  depth,
  maximizingPlayer,
}: AlphaBeta): AlphaBetaReturn {
  movesAnalised++;
  let bestMove: Move | null = null;
  if (depth === 0) {
    return [evaluateBoard(game), null];
  }

  const possibleMoves = game.moves({ verbose: true }) as Move[];
  // Sort randomly to avoid same moves being chosen every time
  possibleMoves.sort(() => 0.5 - Math.random());

  let maxValue = Number.NEGATIVE_INFINITY;
  let minValue = Number.POSITIVE_INFINITY;

  for (const move of possibleMoves) {
    game.move(move);

    const [childValue, _] = minimax({
      game,
      alpha,
      beta,
      depth: depth - 1,
      maximizingPlayer: !maximizingPlayer,
    });

    game.undo();

    if (maximizingPlayer) {
      if (childValue > maxValue) {
        maxValue = childValue;
        bestMove = move;
      }
      if (childValue > alpha) {
        alpha = childValue;
      }
    } else {
      if (childValue < minValue) {
        minValue = childValue;
        bestMove = move;
      }
      if (childValue < beta) {
        beta = childValue;
      }
    }

    if (alpha >= beta) {
      break;
    }
  }

  return maximizingPlayer ? [maxValue, bestMove] : [minValue, bestMove];
}

function calculateBestMove(depthLvl: number): [Move, number] {
  movesAnalised = 0;
  let alpha = Number.NEGATIVE_INFINITY;
  let beta = Number.POSITIVE_INFINITY;
  let move = chess.moves({ verbose: true })[0] as Move;

  const [bestScore, bestMove] = minimax({
    game: chess,
    alpha,
    beta,
    depth: depthLvl,
    maximizingPlayer: true,
  });

  return bestMove === null ? [move, bestScore] : [bestMove, bestScore];
}
```

**Good to know:**

There is a thing called [The horizon effect](https://www.chessprogramming.org/Horizon_Effect), which is caused by limited depth of the search algorithm. You can further reduce it by adding _quiescence search_.

## More humane AI

To soft things off, I added audio to the AI, so it now not only it does kick my ass but it does vocalize it as well.

```typescript
type  playAudioParams  =  {
	chess: Chess;
	move: Move;
	isPlayer: boolean;
};
export  async  function  playAudioOnMove({  chess,  move,  isPlayer  }:  playAudioParams)  {
	const flags  =  move.flags  as  MOVE_FLAGS;
	const audioData  =  isPlayer  ?  defensiveAudio  :  ofensiveAudio;
	const piece  =  move.piece;

	if (chess.isCheck()) {
	const audio = new  Audio(audioData.check);
	await playAudio(audio);
	return;
	}

	if (chess.isCheckmate()) {
	const audio = new Audio(audioData.check);
	await playAudio(audio);
	return;
}

const audio = audioData[flags]?.[piece];
	if (audio) {
	await playAudio(new Audio(audio));
	}
}

function playAudio(audio: HTMLAudioElement) {
	return new Promise((res) => {
	audio.play();
	audio.onended = res;
});
```

Audio data schema and rest of functionality available here: [source code](https://github.com/Danielratmiroff/chess-ai/tree/master/src/lib)

## Outro

I encorage you to try it out and play a game here 👌❤️: [Play a game](https://chess-ai-danielratmiroff.vercel.app/)

Hope you have a fun time!

## UI Design:

![Screenshot](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/chessai/ai-screenshot.png)\
