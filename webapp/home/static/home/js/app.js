var cameraStarting = false;
var cameraEventsBound = false;

function setCameraStatus(message) {
    $('#camera-status').text(message);
}

function startCamera() {
    if (!window.Webcam) {
        console.error('Webcam.js failed to load.');
        setCameraStatus('Camera support failed to load. Refresh the page and try again.');
        return;
    }

    if (cameraStarting || Webcam.loaded) {
        return;
    }

    cameraStarting = true;
    setCameraStatus('Starting camera. Please allow camera access when prompted.');
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
    });

    if (!cameraEventsBound) {
        Webcam.on('load', function() {
            console.log('Webcam loaded successfully.');
            cameraStarting = false;
            setCameraStatus('Camera ready. Position an object and take a snapshot.');
        });

        Webcam.on('error', function(err) {
            console.error(err);
            cameraStarting = false;
            setCameraStatus('Camera unavailable. Check camera permission, then click Take Snapshot to retry.');
        });
        cameraEventsBound = true;
    }

    Webcam.attach('#camera');
}

function key() {
    startCamera();
}

function said(word) {
    var su = new SpeechSynthesisUtterance();
    su.lang = "en";
    su.text = word;
    speechSynthesis.speak(su);
}

function speakDetectedLabels(data) {
    var labels = Array.isArray(data && data.label) ? data.label : [];
    var cleanLabels = labels.filter(Boolean).map(String);

    if (!cleanLabels.length) {
        $('#result-text').text('No objects detected. Please try again.');
        setCameraStatus('No objects detected. Point the camera at a recognizable object and try again.');
        return false;
    }

    var spokenText = cleanLabels.join(', ');
    $('#result-text').text(spokenText);
    said(spokenText);
    return true;
}

function take_snapshot() {
    if (!window.Webcam || !Webcam.loaded) {
        if (!cameraStarting) {
            startCamera();
        }
        setCameraStatus('Camera is not ready yet. Allow access or wait for it to start, then try again.');
        return;
    }

    $('#take-snapshot').prop('disabled', true).val('Detecting...');
    setCameraStatus('Capturing image and detecting objects...');
    Webcam.snap(function(data_uri) {
        $.ajax({
            url: '/savepic',
            type: 'POST',
            data: data_uri,
            dataType: 'json',
            success: function(data) {
                $('#res').attr('src', '/static/home/images/img.jpg?time=' + new Date().getTime());
                if (speakDetectedLabels(data)) {
                    setCameraStatus('Detection complete. Position another object to continue.');
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText || 'Snapshot failed.');
                setCameraStatus('Unable to process the snapshot. Please try again.');
            },
            complete: function() {
                $('#take-snapshot').prop('disabled', false).val('Take Snapshot');
            }
        });
    });
}
