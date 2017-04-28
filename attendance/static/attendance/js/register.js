function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#profile-pic').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_profile_picture").change(function(){
    readURL(this);
});

