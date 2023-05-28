document.addEventListener('DOMContentLoaded', function() {
  document.querySelector("#addSubtask").addEventListener('click', addSubtask);
});

function addSubtask() {
  console.log("addsubtask");

  let subtaskForm = document.querySelectorAll(".subtask-form");
  let container = document.querySelector(".subtask-form-container");
  let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
  let formNum = subtaskForm.length - 1;

  let newForm = subtaskForm[0].cloneNode(true);
  let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number
  formNum++;
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`); //Update the new form to have the correct form number

  container.insertBefore(newForm, document.querySelector("#addSubtask")); //Insert the new form at the end of the list of forms
  totalForms.setAttribute('value', `${formNum+1}`); //Increment the number of total forms in the management form
}

/*
function toggleComplete() {
  console.log(this.value)
//  this.disabled = true;
//  setTimeout(function() {this.disabled = false;}, 10000);
  fetch("tasks", { method: 'PUT',
    body: JSON.stringify({ primaryKey: this.value}),
    csrfmiddlewaretoken: $('#csrf-helper input[name="csrfmiddlewaretoken"]').attr('value'),
    credentials: 'same-origin',
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    } })
  .then(() => {
    window.location = window.location;
  });
}

function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;}

function changeView(view) {
  let tasks = new Array();
  fetch("tasks/"+view)
  .then(response => {
    response.forEach(function(task) {
      tasks.append(task.json())
    })
  })
  .then(function () {
    if (tasks.length == 0) {
      document.querySelector(".tasks-container").innerHTML = `<h3>You have no tasks.</h3>`;
    } else {
      document.querySelector(".tasks-container").innerHTML = '';
      tasks.forEach(function() {
        document.querySelector(".tasks-container").innerHTML += ``;
      });
    }
  })
}

function addTask() {
  console.log("addtask")
  //get form inputs
  //let taskContent = document.getElementsByName("content").value;
  //let taskStartDay = document.getElementsByName("start-time").value;
  //let taskEndDay = document.getElementsByName("end-time").value;

  //create a task, which is a json object
  fetch('/tasks', {method: 'POST',
  body: JSON.stringify({
      content: taskContent,
      start: taskStartDay,
      end: taskEndDay
    })
  })
  .then(location.reload())
}
function subtask() {
  let form = document.querySelector('.subtasks-form-container');
  let subtask = document.createElement('div');
  subtask.classList.add('subtask-form');
  subtask.innerHTML = `<textarea required></textarea><br />
                        No Start Day<input type="checkbox" name="no-start">
                        <input type="datetime-local" name="start-time${subtaskNum}">
                        <input type="datetime-local" name="end-time${subtaskNum}" required>
                        All Day<input type="checkbox" name="all-day">
                        <input type="checkbox" name="all-day${subtaskNum}">`;
  form.appendChild(subtask);
  subtaskNum++;
}
*/
