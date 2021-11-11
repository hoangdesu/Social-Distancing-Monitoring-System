import React from 'react';
import Webcam from 'react-webcam';

const Live = () => {
    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: 'user',
    };
    const webcamRef = React.useRef(null);

    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
    }, [webcamRef]);

    return (
        <div>
            CAM1
            <Webcam
                audio={false}
                height={360}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={360}
                videoConstraints={videoConstraints}
            />
            CAM2
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
            />
        <button onClick={capture}>Capture</button>
        </div>
    );
};

export default Live;
