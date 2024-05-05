$(document).ready(function() {

    $('#all_classes').change(function(){

      $.getJSON('/_update_dropdown', {
        selected_class: $('#all_classes').val()

      }).done(function(data) {
            $('#all_entries').html(data.html_string_selected);
       })
    });
    $('#process_input').bind('click', function() {

        $.getJSON('/_process_data', {
            selected_class: $('#all_classes').val(),
            selected_entry: $('#all_entries').val(),


        }).success(function(data) {
            $('#processed_results').text(data.random_text);
        })
      return false;

    });
  });