let list = []

class Task {
    constructor(name, dueDate) {
        this.taskId = Date.now();
        this.name = name;
        this.dueDate = dueDate;
    }

    toString() {
        let htmlText = '<li class="task" ><div>'
        htmlText += this.name
        htmlText += ", " + this.dueDate.getDate() 
                 + "/" + this.dueDate.getMonth();
        htmlText += '<button onclick="deleteTask(';
        htmlText += this.taskId;
        htmlText += ')">Delete</button>';
        htmlText += '</div></li>';
        return htmlText;
    }
}

function render() {
    const listUI = document.getElementById("todolist")
    listUI.innerHTML = "";
    if (list.length === 0) listUI.innerHTML = "No tasks todo :-)"
    list.forEach((task) => {
        listUI.innerHTML += task.toString();
    })
}

function deleteTask(taskId) {
    list = list.filter(
        (t) => {
            if(t.taskId != taskId) 
            return t;
        }
    );

    render()
}

function createTask() {
    const taskName = document.getElementById("taskName").value;
    addTask(new Task(taskName, new Date()));
}

function addTask(t) {
    list.push(t)
    render();
}

function main() {
    addTask(task);
 
}

main();