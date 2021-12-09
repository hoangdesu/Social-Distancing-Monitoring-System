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
    // const [videoSrc, setVideoSrc] = useState(<img src="http://192.168.1.6:8000/video_feed" alt=""></img>);


    // testing data stream from server
    const [counter, setCounter] = useState(0);
    // const [imageData, setImageData] = useState('');

    
    // using Flask server
    const VIDEO_FEED_URL = 'http://192.168.1.6:8000/video_feed'

    // useEffect(() => {
    //     console.log("LIVE!!");
    //     // axios.get(VIDEO_FEED_URL)
    //     //     .then(data => {
    //     //         console.log("Video:", data);
    //     //     })
    //     //     .catch(e => {
    //     //         console.log("Error:", e);
    //     //     })
    //     // fetch(VIDEO_FEED_URL)
    //     //     .then(res => {
    //     //         if (res.ok) {
    //     //             console.log("Fetched video OK");
    //     //         } else {
    //     //             console.log("fetched error")
    //     //         }
    //     //     })
    //     //     .catch(e => {
    //     //         console.log(e);
    //     //     })

        
    // }, []);

    const socket = io('ws://localhost:5000/');
    // TESTING SOCKET IO
    useEffect(() => {

        // window.location.reload();
        console.log(socket);

        socket.on("connect", data => {
            console.log("connected");
            socket.send("from react");
            socket.emit('sum', {num: [1, 9]}, (res) => {
                console.log(res);
            })
        })

        socket.on("t1", (r) => {
            console.log(r);
        })
        
        socket.on('message', (data) => {
            console.log('message:', data);
        })

        socket.on('chart-data', (data) => {
            console.log('CHART DATA:', data);
        })

        socket.on('counter', data => {
            console.log("Counter:", data)
            setCounter(data)
        })

        socket.on('video-stream', data => {
            console.log("Got the frame", data.slice(0, 10))
            const prefix = 'data:image/jpeg;charset=utf-8;base64, ';
            console.log(prefix + data + '\n')
            document.getElementById("image_data").src=(prefix + data);
            // setImageData(prefix + data);
        })

        socket.on('brian', data => {
            console.log("Counter:", data)
            setCounter(data)
        })

    }, [])



    // const refetchVideo = () => {
    //     fetch(VIDEO_FEED_URL)
    //         .then(res => {
    //             if (res.ok) {
    //                 console.log("Fetched video OK");
    //                 setVideoSrc(<img src="http://192.168.1.6:8000/video_feed" alt=""></img>)
    //             } else {
    //                 console.log("fetched error")
    //             }
    //         })
    //         .catch(e => {
    //             console.log(e);
    //         })
    // }
    

    return (
        <div>
            <img src="http://192.168.0.103:5000/video_feed" alt="" />
            <div style={{ margin: 20 }}>
            <h1 style={{ paddingLeft: 20 }}>QR Reader</h1>
            {/* {videoSrc} */}
            </div>

            {/* <h1>{counter}</h1> */}
            <div style={{ border: '1px solid red'}}>
                <img id="image_data" src="" alt="" />
            </div>

            {/* data:image/jpeg;charset=utf-8;base64,  */}

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
