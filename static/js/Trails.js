$(function(){
    const choosing = JSON.parse(document.getElementById('choosing').textContent);
    if(choosing) chooseTrail();
    else{
        $('.check').click((e)=>{
            e.preventDefault();
            let form=$('#answer-form');
            $('#answer-form #id_answer').val($('#temp-ans').val());
            $.post(form.attr("action"),form.serialize())
                .done((response)=>{
                    if(response.winner) location.reload();
                    const response_div = $('.response');
                    if(response.correct){
                        response_div.html(
                            `<div class="alert alert-success text-center mb-0" role="alert">
                                Correct Answer, Fetching Trails For You!
                            </div>`
                        )
                        setTimeout(chooseTrail,2000)
                        setTimeout(()=> $('.question-block').addClass('hidden'),1900);
                    }
                    else{
                        form[0].reset();
                        $('#temp-ans').val('')
                        response_div.html(
                            `<div class="alert alert-danger text-center mb-0" role="alert">
                                Damn These Questions, Wrong Answer!
                            </div>`
                        )
                        setTimeout(()=>response_div.html(''),2000);
                    }
                })
                .fail(()=>{
                    console.log('Error!!');
                })
        });
        $('.question-block').removeClass('hidden');
    }
})

function chooseTrail(){
    $('.trail').removeClass('hidden');

    $('.trail button').click((e)=>{

        let csrftoken = getCookie('csrftoken');
        setRequestHeader(csrftoken);
        $.post(e.target.dataset.url,{'trail': e.target.value})
        .done((response)=>{
            if(response.success) location.reload();
        })
        .fail(()=>{
            console.log('Error!!');
        })
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
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function to set Request Header with `CSRFTOKEN`
function setRequestHeader(csrftoken){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}