const { exec } = require('child_process');
const path = require('path');

// Define the output file path
const outputFile = path.join(__dirname, '../images/test_photo.jpg');

// FFmpeg command
const ffmpegCommand = `ffmpeg -f avfoundation -framerate 30 -video_size 1280x720 -i "1" -frames:v 1 ${outputFile} -y`;

// Execute the command
exec(ffmpegCommand, (error, stdout, stderr) => {
    if (error) {
        console.error('Error capturing photo:', error.message);
        return;
    }
    if (stderr) {
        console.error('FFmpeg error output:', stderr);
    }
    console.log('Photo captured successfully and saved at:', outputFile);
});
