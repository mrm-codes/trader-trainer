//Dropdown navigation

function drop () {
    var elem = document.getElementById('drop-btn');
    elem.classList.toggle('dropit');

    var elem_item = document.getElementById('dropdown-item');

    if (elem.classList.contains('dropit')){
        elem_item.classList.add('show-element')
    } 

};