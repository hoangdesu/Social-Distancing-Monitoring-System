import React, { useState, useEffect } from 'react';
import axios from 'axios';

import DashboardCSS from './Dashboard.module.css';

import InfoPanel from './InfoPanel';

// API ENDPOINTS
const LATEST_MEASUREMENTS = 'http://localhost:7000/measurements/latest/';
const VIDEO_FEED = 'http://192.168.137.51:5000/video_feed';
const ALL_ENTRY = 'http://localhost:7000/entry/all';
const LATEST_MESSAGE = 'http://localhost:7000/message/latest';
const UPDATE_INTERVAL = 1000 * 2; // ms

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
                setMeasurements((prev) => ({
                    ...prev,
                    temperature: Math.floor(Math.random() * 50),
                    humidity: Math.floor(Math.random() * 100),
                })); // for testing only
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
            {/* <h2>Measurements</h2> */}
            <InfoPanel measurements={measurements} peopleNum={peopleNum} />

            <div
                id="qr-mask"
                className={`${DashboardCSS['card']} ${DashboardCSS['medium-element']}`}
            >
                <div>
                    <img src={VIDEO_FEED} alt="QR_Camera" />
                </div>
                {/* <h3>Total people</h3>
                    <Line options={options} data={data1} /> */}
            </div>
        </div>
    );
};

export default Dashboard;
