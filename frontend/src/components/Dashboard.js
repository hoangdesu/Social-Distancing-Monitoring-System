import React, { useState, useEffect } from 'react';
import axios from 'axios';

import DashboardCSS from './Dashboard.module.css';
import InfoPanel from './InfoPanel';

// API ENDPOINTS
const LATEST_MEASUREMENTS = 'http://localhost:7000/measurements/latest/';
const QR_VIDEO_FEED = 'http://192.168.137.5:5000/video_feed';
const CAMERA_VIDEO_FEED = 'http://192.168.137.27:9099/video_feed';
const ALL_ENTRY = 'http://localhost:7000/entry/latest';
const LATEST_MESSAGE = 'http://localhost:7000/message/latest';
const UPDATE_INTERVAL = 1000 * 0.5; // 2s

const Dashboard = () => {
    // --- STATES ---
    const [measurements, setMeasurements] = useState({
        temperature: 27,
        moisture: 1,
        humidity: 2,
        created: 'Created Time (placeholder)',
    });
    const [peopleNum, setPeopleNum] = useState(0);
    const [peopleIn, setPeopleIn] = useState(0);
    const [peopleOut, setPeopleOut] = useState(0);
    const [serverConnected, setServerConnected] = useState(false);
    const [camIsOn, setCamIsOn] = useState(false);
    const [message, setMessage] = useState("")
    // --- FUNCTIONS ---
    const fetchMeasurements = () => {
        axios
            .get(LATEST_MEASUREMENTS)
            .then((res) => {
                let celcius = res.data[0].celcius;
                let moisture = res.data[0].moisture;
                let humidity = res.data[0].humidity;

                console.log(res.data[0])
                // condition checks before setting measurements
                if (parseFloat(celcius) !== 0) {
                    setMeasurements((prev) => ({
                        ...prev,
                        temperature: celcius,
                    }));
                }
                if (parseFloat(moisture) !== 0) {
                    setMeasurements((prev) => ({
                        ...prev,
                        moisture: moisture,
                    }));
                }
                if (parseFloat(humidity) !== 0) {
                    setMeasurements((prev) => ({
                        ...prev,
                        humidity: humidity,
                    }));
                }
            })
            .catch((e) => {
                setServerConnected(false);

                // for testing only
                setMeasurements((prev) => ({
                    ...prev,
                    temperature: Math.floor(Math.random() * 50),
                    humidity: Math.floor(Math.random() * 100),
                    moisture: Math.floor(Math.random() * 100),
                })); 
                console.log('Error fetching measurements -', e);
            });
    };

    const fetchPeopleNumberInRoom = () => {
        axios
            .get(ALL_ENTRY)
            .then((res) => {
                let entry_number = parseInt(res.data[0].entry_number);
                let in_number = parseInt(res.data[0].current_in);
                let out_number = parseInt(res.data[0].current_out);

                if (parseInt(entry_number) < 0) entry_number = 0;
                if (parseInt(in_number) < 0) in_number = 0;
                if (parseInt(out_number) < 0) out_number = 0;

                setPeopleNum(entry_number);
                setPeopleIn(in_number);
                setPeopleOut(out_number);
            })
            .catch((e) => {
                setServerConnected(false);
                console.log('Error fetching number of people in room -', e);
            });
    };

    const fetchLatestMessage = () => {
        axios
            .get(LATEST_MESSAGE)
            .then((res) => { 
                if (res.data[0] !== undefined) {
                    let content = res.data[0].content
                    if (content === 'Program Start') {
                        setServerConnected(true)
                    }
                    if (content === 'QR Scan is done') {
                        setCamIsOn(false)
                    } else if (content === 'QR Check!') {
                        setCamIsOn(true)
                    }
                    else if (content !== 'QR Check!' && content !== 'QR Scan is done') {
                        setCamIsOn(false)
                    }
                    setMessage(content)
                }
                console.log(message)
                console.log(camIsOn)
            })
            .catch((e) => {
                console.log('Error fetching latest message -', e);
            });
    };

    // only for testing graph responsive data
    const changePpl = (option) => {
        if (option === 'add') {
            setPeopleNum((prev) => {
                if (prev >= 0 && prev < 5) return prev + 1;
                else return prev;
            });
        } else if (option === 'remove') {
            setPeopleNum((prev) => {
                if (prev > 0 && prev <= 5) return prev - 1;
                else return prev;
            });
        }
    };

    // --- EFFECTS ---
    useEffect(() => {
        setInterval(() => {
            fetchMeasurements();
            fetchPeopleNumberInRoom();
            fetchLatestMessage();
        }, UPDATE_INTERVAL);
    }, []);

    return (
        <div className={DashboardCSS.container}>
            <div className={DashboardCSS['first-row']}>
                <h2>Raspberry Pi Program Status: {serverConnected ? 'connected' : 'connecting...'}</h2>
            </div>
            <div className={DashboardCSS['second-row']}>
                <InfoPanel measurements={measurements} peopleNum={peopleNum} peopleIn={peopleIn} peopleOut={peopleOut} />
            </div>
            <div>
                <div
                    className={`${DashboardCSS['card']}`}
                >
                    <h2>Message: {message}</h2>
                    <h2 style={{paddingLeft: 1100}}>{camIsOn === true ? 'QR is Reading' : 'QR Reader is on IDLE Mode'}</h2>
                    <img src={CAMERA_VIDEO_FEED} style={{height: 445, paddingRight: 20}}alt="camera video feed" />
                    <img src={QR_VIDEO_FEED} alt="qr camera video feed" style={{height: 445}} /> 
                </div>
            </div>
            
            {/* for testing only
            <div>
                <button onClick={() => changePpl('remove')}>Remove</button>
                <button onClick={() => changePpl('add')}>Add</button>
            </div> */}
        </div>
    );
};

export default Dashboard;
