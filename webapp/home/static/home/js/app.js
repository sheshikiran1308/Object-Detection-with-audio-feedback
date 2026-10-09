function key() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
     });
     Webcam.attach( '#camera' );    
}

function said(word) {
    var su = new SpeechSynthesisUtterance();
    su.lang = "en";
    su.text = word;
    speechSynthesis.speak(su);
  }


function take_snapshot() {
    Webcam.snap( function(data_uri) {
        $.post("/savepic",data_uri, function(data, status){
            $('#res').attr("src","/static/home/images/img.jpg?time=" + new Date().getTime());
            said(data['label'])
          });
    });
}


