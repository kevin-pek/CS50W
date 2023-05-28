document.addEventListener('DOMContentLoaded', function() {
	//LOADS THE DEFAULT BOARD IF FIRST TIME LOADING THE PAGE

	if (!localStorage.getItem("current_board")) {
		localStorage.setItem("current_board", "default");
		loadBoard();
	} else {
		loadBoard(localStorage.getItem("current_board"));
	}

	document.getElementById("create").addEventListener("click", createNote);
});

function loadBoard(boardname="default") {
	//CHANGE CURRENT BOARD TO SELECTED
	localStorage.setItem("current_board", boardname);
	//document.getElementById("dropdownMenuButton").innerHTML = localStorage.getItem("current_board");

	fetch("boards/"+localStorage.getItem("current_board"))
	.then(response => response.json())
	.then(board => {
		board.forEach(note => {
			//GET NOTES FROM DB AND APPEND TO DOM
			let noteElement = document.createElement('div');
			noteElement.classList.add('note');
			//DATASET ID
			noteElement.dataset.key = note.id;
			noteElement.innerHTML = `<button onclick="deleteNote(${note.id})" class="close text-white remove-form" aria-label="Close">
																	<span aria-hidden="true">&times;</span>
																</button>
																<textarea oninput="updateNote(this.parentElement)">${note.content}</textarea>`;

			noteElement.style.left = note.x_coord+"px";
			noteElement.style.top = note.y_coord+"px";
			noteElement.dataset.x = 0;
			noteElement.dataset.y = 0;
			noteElement.style.width = note.width+"px";
			noteElement.style.height = note.height+"px";

			document.querySelector('.board').append(noteElement);
		})
	})
}

function updateNote(note) {
	fetch("boards/"+note.dataset.key+"/save", {
		method: "PUT",
		body: JSON.stringify({
			content: note.lastElementChild.value,
			x_coord: parseInt(note.style.left) + parseInt(note.dataset.x),
			y_coord: parseInt(note.style.top) + parseInt(note.dataset.y),
			width: parseInt(note.style.width),
			height: parseInt(note.style.height)
		}),
	})
}

function createNote() {
	//CREATE AND SAVE NEWNOTE TO DB
	fetch("boards/"+localStorage.getItem("current_board")+"/add")
	.then(response => response.json())
	.then(note => {
		//APPEND TO DOM
		let noteElement = document.createElement("div");
		noteElement.classList.add("note");
		noteElement.innerHTML = `<button onclick="deleteNote(${note.id})" class="close text-white remove-form" aria-label="Close">
																<span aria-hidden="true">&times;</span>
															</button>
															<textarea oninput="updateNote(this.parentElement)"></textarea>`;
		noteElement.style.left = window.innerWidth / 2 + "px";
		noteElement.style.top = window.innerHeight / 2 + "px";
		noteElement.dataset.x = 0;
		noteElement.dataset.y = 0;
		noteElement.style.width = "200px";
		noteElement.style.height = "200px";
		noteElement.dataset.key = note.id;
		document.querySelector('.board').append(noteElement);
	})
}

function deleteNote(id) {
	fetch("boards/delete/"+id)
	.then(location.reload())
}
