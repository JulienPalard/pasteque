function refresh_characters_left() {
    var characters_left = parseInt(document.getElementById("max_characters").value) - $('#id_content').val().length;
  $('b#charsleft_counter').html(characters_left);
}
$(document).ready(function() {
  refresh_characters_left();
});
$('#id_content').keyup(function() {
  refresh_characters_left();
})
