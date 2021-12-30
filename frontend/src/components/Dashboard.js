import React, { useState, useEffect } from 'react';
import axios from 'axios';

import DashboardCSS from './Dashboard.module.css';

import InfoPanel from './InfoPanel';

// API ENDPOINTS
const LATEST_MEASUREMENTS = 'http://localhost:7000/measurements/latest/';
const VIDEO_FEED = 'http://192.168.137.51:5000/video_feed';
const ALL_ENTRY = 'http://localhost:7000/entry/all';
const LATEST_MESSAGE = 'http://localhost:7000/message/latest';
const UPDATE_INTERVAL = 1000 * 2; // 2s

const Dashboard = () => {
    // --- STATES ---
    const [measurements, setMeasurements] = useState({
        temperature: 27,
        moisture: 1,
        humidity: 2,
        created: 'Created Time (placeholder)',
    });
    const [peopleNum, setPeopleNum] = useState(0);
    const [serverConnected, setServerConnected] = useState(false);
    const [camIsOn, setCamIsOn] = useState(false);

    // --- FUNCTIONS ---
    const fetchMeasurements = () => {
        axios
            .get(LATEST_MEASUREMENTS)
            .then((res) => {
                let { celcius, moisture, humidity } = res.data[0].celcius;

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
                let { entry_number } = parseInt(res.data[0]);
                if (parseInt(entry_number) < 0) entry_number = 0;
                setPeopleNum(entry_number);
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
                let { content } = res.data[0];
                if (content === 'QR Scan is done') {
                    // update QR scan camera
                } else if (content === 'QR Check!') {
                    // update QR scan camera
                }
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
            <h2>Server status: {serverConnected ? 'connected' : 'connecting...'}</h2>
            {/* <h2>Measurements</h2> */}
            <InfoPanel measurements={measurements} peopleNum={peopleNum} />

            {/* for testing only */}
            <div>
                <button onClick={() => changePpl('remove')}>Remove</button>
                <button onClick={() => changePpl('add')}>Add</button>
            </div>

            <h2>Camera</h2>
            <div className={DashboardCSS.card}>
                <img src={VIDEO_FEED} alt="QR_Camera" />
            </div>

{/* 
            <div
                id="qr-mask"
                className={`${DashboardCSS['card']} ${DashboardCSS['medium-element']}`}
            >
                <div>
                    <img src={VIDEO_FEED} alt="QR_Camera" />
                </div>
            </div> */}
        </div>
    );
};

export default Dashboard;
