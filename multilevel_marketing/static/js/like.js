$(document).ready(function(){
    $(".icon-heart").click(function(event){
        event.preventDefault()
      event.stopPropagation()
        var attr_id = $(this).attr('attr_id');
        var action_url = $(this).attr('action_url');
        var that = $(this);
        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        $.ajax({
            url: action_url,
            type: "POST",
            data: {'attr_id': attr_id,'csrfmiddlewaretoken': '{{csrf_token}}' },
            beforeSend: function(xhr){xhr.setRequestHeader('X-CSRFToken', "{{csrf_token}}");},
            success: function (result) {
                console.log("Success")
                that.toggleClass("heart");
            },
            

        });
    });
});
