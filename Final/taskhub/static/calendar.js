//adds function to do addition/subtraction of dates
Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

Element.prototype.documentOffsetTop = function () {
    return this.offsetTop + ( this.offsetParent ? this.offsetParent.documentOffsetTop() : 0 );
};

var today = new Date();
today.setHours(0,0,0,0);
var selectedDay = new Date(today.getFullYear(), today.getMonth(), 1); //first day of selected month

//display the 5 weeks around a month, firstDay must be a Sunday, lastDay a Saturday
let multiple = Math.floor(window.innerHeight / 130 * 7 / 2);
console.log(multiple)
var firstDay = today.addDays(-(multiple)-today.getDay()); //getDay, 0 for Sunday, 6 for Saturday
var lastDay = today.addDays((multiple)+today.getDay());

document.addEventListener('DOMContentLoaded', function() {
  let dateRange = getDates(firstDay, lastDay);
  dateRange.forEach(loadNext);
  updateMonth(today);

  window.scrollTo({
    top: document.querySelector('.current-day').documentOffsetTop() - (window.innerHeight / 2),
    behavior: 'smooth'});

  updateTasks();
  //make sure the days of week corresponds to the dates on the calendar grid
  /*let css = ".date-grid .date-cell:first-child { grid-column: " + 0 + "; }";
  let style = document.createElement('style');
  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
      style.appendChild(document.createTextNode(css));
  }
  document.getElementsByTagName('head')[0].appendChild(style);*/
});

window.onscroll = () => {
  //scroll down
  if (window.innerHeight + window.scrollY >= document.querySelector('.date-grid').offsetHeight - 100) {
    let dateRange = getDates(lastDay.addDays(1), lastDay.addDays(7));
    lastDay = lastDay.addDays(7);
    firstDay = firstDay.addDays(7);
    dateRange.forEach(loadNext);
    removeCells(true);

    //console.log(lastDay);

    //check for condition to change selected month
    if (lastDay.getMonth() - 1 > selectedDay.getMonth() || lastDay.getFullYear() > selectedDay.getFullYear()) {
      selectedDay.setMonth(selectedDay.getMonth()+1);
    //  console.log(selectedDay);
    }
    updateMonth(selectedDay);
  }

  //scroll up
  if (window.scrollY <= 50) {
    let dateRange = getDates(firstDay.addDays(-7), firstDay.addDays(-1)).reverse();
    lastDay = lastDay.addDays(-7);
    firstDay = firstDay.addDays(-7);
    dateRange.forEach(loadPrevious);
    removeCells(false);

    //console.log(firstDay);

    //check for condition to change selected month
    if (firstDay.getMonth() + 1 < selectedDay.getMonth() || firstDay.getFullYear() < selectedDay.getFullYear()) {
      selectedDay.setMonth(selectedDay.getMonth()-1);
    //  console.log(selectedDay);
    }
    updateMonth(selectedDay);
  }

  updateTasks();
}

//CHANGES CLASSES TO HIGHLIGHT
function updateMonth(date) {
  let month = date.toLocaleDateString(undefined, {month: 'long'}) + " " + date.getFullYear();
  document.querySelector('.calendar-navigator > h2').innerHTML = month;

  document.querySelectorAll('.current-month').forEach((cell) => {cell.classList.remove("current-month")});
  let dateRange = getDates(firstDay, lastDay);
  dateRange.forEach((date) => {
    if (date.getMonth() == selectedDay.getMonth()) {
      Array.from(document.getElementsByClassName(selectedDay.getMonth())).forEach((cell) => {
        cell.classList.add("current-month")});
    }
  });
}

//RETURNS ARRAY CONTAINING RANGE OF DATES
function getDates(startDate, stopDate) {
    let dateArray = new Array();
    let currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push(new Date (currentDate));
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
}

//TO LOAD NEW CELLS WHEN SCROLLING DOWN
function loadNext(date, index, array) {
  let cell = document.createElement("div");
//add additional classes for dates in the current month/day
  if (date.getMonth() == selectedDay.getMonth()) {
    cell.classList.add("current-month");
  }
  if (date.getDate() == today.getDate() && date.getMonth() == today.getMonth() && date.getFullYear() == today.getFullYear()) {
    cell.id = "current-day";
  }
  cell.classList.add("date-cell");
  cell.classList.add(date.getMonth());
  cell.innerHTML = `<time datetime="${date.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'})}">${date.getDate()}</time>`;
  document.querySelector(".date-grid").appendChild(cell);
}

//TO LOAD NEW CELLS WHEN SCROLLING UP
function loadPrevious(date, index, array) {
  let cell = document.createElement("div");
//add additional classes for dates in the current month/day
  if (date.getMonth() == selectedDay.getMonth()) {
    cell.classList.add("current-month");
  }
  if (date.getDate() == today.getDate() && date.getMonth() == today.getMonth() && date.getFullYear() == today.getFullYear()) {
    cell.id = "current-day";
  }
  cell.classList.add("date-cell");
  cell.classList.add(date.getMonth());
  cell.innerHTML = `<time datetime="${date.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'})}">${date.getDate()}</time>`;
  document.querySelector(".date-grid").prepend(cell);
}

//REMOVES EITHER TOP OR BOTTOM ROW OF CELLS
function removeCells(scrollDown) {
  let grid = document.querySelector('.date-grid')
  let i = 0;
  if (!scrollDown) {
    while (i<7) {
      grid.removeChild(grid.lastElementChild);
      i++;
    }
  } else {
    while (i<7) {
      grid.removeChild(grid.firstElementChild);
      i++;
    }
  }
}

function updateTasks() {
  //GET INCOMPLETE USER TASKS AND SHOW IN CALENDAR
  fetch("calendar/get_tasks")
  .then(response => response.json())
  .then(tasks => {
    $('.task-cell').remove();
    tasks.forEach(task => {
      //insert task into corresponding date cells
      //console.log(task);

      let taskCell = document.createElement('div');
      taskCell.classList.add("task-cell");
      taskCell.id = "task"+task.id;
      taskCell.innerHTML = `${task.content}`;
      let date = new Date(task.deadline);
      date.setHours(0,0,0,0);
      //console.log(date);

      if (task.start) {
        let d=new Date(task.start)
        d.setHours(0,0,0,0);

        while (d <= date) {
          try {
            console.log(d.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'}));
            console.log(taskCell.cloneNode(true));

            document.querySelector(`[datetime="${d.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'})}"]`).parentNode.append(taskCell.cloneNode(true));
          } catch {
            console.log("failed.");
          }
          d.setDate(d.getDate()+1)
        }
      } else {

        try {
          document.querySelector(`[datetime='${date.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'})}']`).parentNode.append(taskCell.cloneNode(true));
        } catch {
          console.log("failed.");
        }
      }
    })
  });
}
