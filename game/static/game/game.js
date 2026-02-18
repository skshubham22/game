const roomCode = JSON.parse(document.getElementById('room-code').textContent);
const gameType = JSON.parse(document.getElementById('game-type').textContent);
const statusDiv = document.getElementById('status');
const boardDiv = document.getElementById('game-board');

let socket;
let mySide = null;
let currentTurn = null;

function connect() {
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(
        wsScheme + '://' + window.location.host + '/ws/game/' + roomCode + '/'
    );

    socket.onopen = function (e) {
        console.log('Chat socket opened');
        document.getElementById('connection-status').innerText = 'Connected';
        document.getElementById('connection-status').style.color = '#55efc4';
        socket.send(JSON.stringify({
            'type': 'join_game'
        }));
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Message:', data);

        if (data.type === 'game_start') {
            mySide = data.side;
            renderBoard(data.game_state);
        } else if (data.type === 'game_update') {
            renderBoard(data.game_state);
        }
    };

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
        document.getElementById('connection-status').innerText = 'Disconnected - Refresh Page';
        document.getElementById('connection-status').style.color = '#ff7675';
    };
}

function renderBoard(gameState) {
    boardDiv.innerHTML = '';
    const board = gameState.board;
    currentTurn = gameState.turn;
    const winner = gameState.winner;
    const players = gameState.players;

    renderPlayers(players, currentTurn);

    if (winner) {
        if (winner === 'DRAW') {
            statusDiv.innerText = 'Game Over! It\'s a Draw!';
        } else {
            statusDiv.innerText = `Game Over! Winner: ${winner}`;
        }
    } else {
        // Find my name
        let myName = 'You';
        // Need to identify myself from players list using mySide? 
        // Logic: if players contains mySide, that's me.

        statusDiv.innerText = `Turn: ${currentTurn}`;
    }

    if (gameType === 'TIC_TAC_TOE') {
        renderTicTacToe(board, winner);
    }
}

function renderPlayers(players, currentTurn) {
    const listDiv = document.getElementById('players-list');
    listDiv.innerHTML = '';

    // Convert players dict to array
    Object.values(players).forEach(p => {
        const pDiv = document.createElement('div');
        pDiv.classList.add('player-card');
        if (p.side === currentTurn) {
            pDiv.classList.add('active');
        }

        const nameDiv = document.createElement('div');
        nameDiv.classList.add('name');
        nameDiv.innerText = p.name + (p.side === mySide ? ' (You)' : '');

        const sideDiv = document.createElement('div');
        sideDiv.classList.add('side');
        sideDiv.innerText = `Player ${p.side}`;

        pDiv.appendChild(nameDiv);
        pDiv.appendChild(sideDiv);
        listDiv.appendChild(pDiv);
    });
}

function renderTicTacToe(board, winner) {
    board.forEach((cell, index) => {
        const cellDiv = document.createElement('div');
        cellDiv.classList.add('cell');
        if (cell) {
            cellDiv.classList.add('taken');
            cellDiv.classList.add(cell.toLowerCase());
            cellDiv.innerText = cell;
        }

        cellDiv.onclick = () => {
            if (!cell && !winner && mySide === currentTurn) {
                makeMove(index);
            }
        };

        boardDiv.appendChild(cellDiv);
    });
}

function makeMove(index) {
    socket.send(JSON.stringify({
        'type': 'make_move',
        'index': index,
        'player': mySide
    }));
}

connect();
