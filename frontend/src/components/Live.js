import React, { useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

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
    const [videoSrc, setVideoSrc] = useState(<img src="http://192.168.1.6:8000/video_feed" alt=""></img>);

    
    // using Flask server
    const VIDEO_FEED_URL = 'http://192.168.1.6:8000/video_feed'

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
                    setVideoSrc(<img src="http://192.168.1.6:8000/video_feed" alt=""></img>)
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
            <h1>QR Reader</h1>
            {/* <img src="http://192.168.1.6:8000/video_feed" alt="" /> */}
            {videoSrc}
            <button onClick={refetchVideo}>Refetch video</button>
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
