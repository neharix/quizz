let table = document.querySelector("#table-body");
let challenge_pk = JSON.parse(document.querySelector("#challenge-pk").textContent);

function success(data) {
    table.innerHTML = "";
    data.forEach(row => {
        let table_row = document.createElement("tr");
        let cell_id = document.createElement("td");
        cell_id.innerHTML = row.id;
        let cell_full_name = document.createElement("td");
        cell_full_name.innerHTML = row.last_name + " " + row.first_name;
        let cell_start = document.createElement("td");
        cell_start.innerHTML = row.start;
        let cell_end = document.createElement("td");
        cell_end.innerHTML = row.end;
        let cell_true = document.createElement("td");
        cell_true.innerHTML = row.true_answer;
        let cell_false = document.createElement("td");
        cell_false.innerHTML = row.false_answer;
        let cell_empty = document.createElement("td");
        cell_empty.innerHTML = row.empty_answer;
        let cell_percent = document.createElement("td");
        cell_percent.innerHTML = row.percent + "%";
        let cell_status = document.createElement("td");
        if (row.is_finished){
            cell_status.classList.add('true');
            cell_status.innerHTML = "<b>Tamamlady</b>";
        } else {
            cell_status.classList.add('false');
            cell_status.innerHTML = "<b>Dowam edýär</b>";    
        }
        table_row.appendChild(cell_id);
        table_row.appendChild(cell_full_name);
        table_row.appendChild(cell_start);
        table_row.appendChild(cell_end);
        table_row.appendChild(cell_true);
        table_row.appendChild(cell_false);
        table_row.appendChild(cell_empty);
        table_row.appendChild(cell_percent);
        table_row.appendChild(cell_status);
        table.append(table_row);
    });
}
function update() {
    $.ajax({
        url: "/api/v1/get-current-data/" + challenge_pk + "/",
        type: 'GET',
        dataType: 'json',
        success: success,
    });
}

const updater = setInterval(update, 3000);

update();