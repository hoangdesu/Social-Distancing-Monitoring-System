import React, { useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { io } from "socket.io-client";

const Live = () => {
    // const videoConstraints = {
    //     width: 1280,
    //     height: 720,
    //     facingMode: 'user',
    // };
    // const webcamRef = React.useRef(null);

    // const capture = React.useCallback(() => {
    //     const imageSrc = webcamRef.current.getScreenshot();
    // }, [webcamRef]);

    // --- video feed states
    const [videoSrc, setVideoSrc] = useState(<img src="http://127.0.0.1:5000/video_feed" alt=""></img>);
    // const [videoSrc, setVideoSrc] = useState(<img src="http://192.168.137.51:5000/video_feed" alt=""></img>);

    // var socket = io('http://192.168.137.51:5000');
    const io = require("socket.io")(httpServer, {  cors: {    
        origin: "https:/127.0.0.1:5000/video_feed",    
        methods: ["GET", "POST"]  
    }});

    socket.on("connect", () => {  
        console.log(socket.id); // ojIckSD2jqNzOqIrAGzL
    });
    // using Flask server
    const VIDEO_FEED_URL = 'https:/127.0.0.1:5000/video_feed'

    useEffect(() => {
        console.log("LIVE!!");
        // axios.get(VIDEO_FEED_URL)
        //     .then(data => {
        //         console.log("Video:", data);
        //     })
        //     .catch(e => {
        //         console.log("Error:", e);
        //     })
        fetch(VIDEO_FEED_URL)
            .then(res => {
                if (res.ok) {
                    console.log("Fetched video OK");
                } else {
                    console.log("fetched error")
                }
            })
            .catch(e => {
                console.log(e);
            })
    }, []);

    const refetchVideo = () => {
        fetch(VIDEO_FEED_URL)
            .then(res => {
                if (res.ok) {
                    console.log("Fetched video OK");
                    setVideoSrc(<img src="http://127.0.0.1:5000/video_feed" alt=""></img>)
                } else {
                    console.log("fetched error")
                }
            })
            .catch(e => {
                console.log(e);
            })
    }

    return (
        <div>
            <script type="text/javascript" charset="utf-8">
            <script src="https://cdn.socket.io/socket.io-1.0.0.js"></script>
            </script>
            {/* <img src="http://192.168.1.6:8000/video_feed" alt="" /> */}
            <div style={{ margin: 20 }}>
            <h1 style={{ paddingLeft: 20 }}>QR Reader</h1>
            {/* {videoSrc} */}
            </div>
            {/* <button onClick={refetchVideo}>Refetch video</button> */}
            {/* CAM2
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
            />
            CAM3
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
                style={{}}
            />
            CAM4
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
            />
            CAM5
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
            />
            CAM6
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
            /> */}
        {/* <button onClick={capture}>Capture</button> */}
        </div>
    );
};

export default Live;
