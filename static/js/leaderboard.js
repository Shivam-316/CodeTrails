const profiles = JSON.parse(document.getElementById('board-data').textContent);
let table = document.getElementById('table')
let table_html=''
profiles.forEach((profile,idx) => {
    table_html+=`
    <tr>
        <th scope="row">${idx+1}</th>
            <td>${profile.user}</td>
            <td>${profile.score}</td>
    </tr>
    `
});
table.innerHTML = table_html