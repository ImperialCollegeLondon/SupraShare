$(document).ready(function() {
    let nRows = 1;

    $('.add_row_button').click(function() {
        ++nRows;
        let newRow = emptyRow.clone(true, true)
        newRow.attr('id', `row${nRows}`)
        $(this).parent().before(newRow);
    });

    $('.predict_button').click(function() {
        // O=Cc1cc(C=O)cc(C=O)c1
        // N[C@H]1CCCC[C@@H]1N
        let row = $(this).parent().parent();
        let bb = row.find('#bb_input').val();
        let lk = row.find('#lk_input').val();
        let model = row.find('select').val();
        // bb = 'O=Cc1cc(C=O)cc(C=O)c1';
        // lk = 'N[C@H]1CCCC[C@@H]1N';
        console.log(bb, lk, model);
        let formData = new FormData();
        formData.append('bb', bb);
        formData.append('lk', lk);

        let request = new XMLHttpRequest();
        request.open('POST', `/predict/${model}`)
        request.addEventListener('load', function() {
            console.log(this.responseText);
            let ans, color;
            if (this.responseText === '1') {
                ans = 'COLLAPSED';
                color = 'red';
            } else {
                ans = 'SHAPE PERSISTENT';
                color = 'green';
            }

            row.find('#ans').empty();
            row.find('#ans').append(`<h2 style="color:${color}">${ans}</h2>`);

        });
        request.send(formData);
    });

    let emptyRow = $('#row1').clone(true, true);
});
