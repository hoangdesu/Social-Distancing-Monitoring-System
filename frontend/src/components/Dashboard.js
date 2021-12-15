import React, { useState, useEffect } from 'react';
import faker from 'faker';
import temp_icon from './../assets/temp-icon.jpg';
import moist_icon from './../assets/moist-icon.jpg';
import humid_icon from './../assets/humid-icon.jpg';
import human_icon from './../assets/people-icon.jpg';
import { Humidity } from 'react-environment-chart';
import DashboardCSS from './Dashboard.module.css';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import "./fontawasome.js"
import { faUser, faStreetView } from '@fortawesome/free-solid-svg-icons';

import Thermometer from './Thermometer';

// API ENDPOINTS
const LATEST_MEASUREMENTS = 'http://localhost:7000/measurements/latest/';
const VIDEO_FEED = 'http://192.168.137.51:5000/video_feed';
const ALL_ENTRY = 'http://localhost:7000/entry/all';
const LATEST_MESSAGE = 'http://localhost:7000/message/latest';
const UPDATE_INTERVAL = 1000 * 5; // ms

// class MyDashBoard extends React.Component {
//     componentDidMount() {
//         this.getData();
//         this.interval = setInterval(() => {
//             this.getData();
//         }, 3000);
//     }

//     getData() {
// axios.get('http://localhost:7000/measurements/latest/').then((res) => {
//     if (parseFloat(res.data[0].celcius) !== 0) {
//         console.log(res.data[0]);
//         document.getElementById('temp-label').innerHTML =
//             'Temperature: ' + res.data[0].celcius + ' °C';
//         document.getElementById('humid-label').innerHTML =
//             'Humidity: ' + res.data[0].humidity + ' %';
//         document.getElementById('moist-label').innerHTML =
//             'Moisture: ' + res.data[0].moisture + ' %';
//         if (res.data[0].created != undefined) {
//             const time = res.data[0].created.split('T');
//             const rm_mili = time[1].split('.');
//             document.getElementById('update-time').innerHTML =
//                 'Last Updated: ' +
//                 time[0] +
//                 ' at ' +
//                 rm_mili[0] +
//                 ' GMT: 0';
//         }
//     }
// });

// axios.get('http://localhost:7000/entry/all').then((res) => {
//     console.log(res.data[0]);

//     if (parseInt(res.data[0].entry_number) < 0)
//         res.data[0].entry_number = '0';
//     document.getElementById('people-label').innerHTML =
//         'Number of people present: ' + res.data[0].entry_number;
// });

// axios.get('http://localhost:7000/message/latest').then((res) => {
//     console.log(res.data[0]);
//     if (res.data[0].content == 'QR Scan is done') {
//         document.getElementById('qr-mask').style.display = 'none';
//     } else if ((res.data[0].content = 'QR Check!')) {
//         document.getElementById('qr-mask').style.display = 'block';
//     }
// });
// }

// componentWillUnmount() {
//     clearInterval(this.interval);
// }

// render() {
//     return <h3 id="update-time">Last Updated: </h3>;
// }
// }

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
            // fetchMeasurements();
            // fetchPeopleNumberInRoom();
            // fetchLatestMessage();
        }, UPDATE_INTERVAL);
    }, []);

    return (
        <div className={DashboardCSS.container}>
            {/* <MyDashBoard /> */}
            <div
                className={`${DashboardCSS['card']} ${DashboardCSS['top-pane']}`}
            >
                {/* <div>
                    <h2>Measurements</h2>
                    
                    <p>Service status: (connected)</p>
                    <p>QR scanner: on</p>
                    <p>(system info)</p>
                </div> */}
                <div>
                    <Thermometer
                        theme="light"
                        value={measurements.temperature}
                        max={50}
                        steps="1"
                        format="°C"
                        size="small"
                        height="150"
                    />
                    <h4>Temperature</h4>    
                </div>
                <div>
                <Humidity
                    value={measurements.humidity}
                    height={100}
                    tips={['10%', '60%', 'three']}
                />
                <h4>Humidity</h4>
                </div>
                <div>
                    <h3>Moisture chart</h3>
                    <p>?</p>
                </div>
                <div>
                <FontAwesomeIcon icon={faStreetView} color='green' size="2x" fixedWidth swapOpacity spin={false} mask={['far', 'circle']}/>
                <FontAwesomeIcon icon={faStreetView} color='green' size="2x" fixedWidth swapOpacity spin={false} mask={['far', 'circle']}/>
                <FontAwesomeIcon icon={faStreetView} color='green' size="2x" fixedWidth swapOpacity spin={false} mask={['far', 'circle']}/>
                <FontAwesomeIcon icon={faStreetView} color='pink' size="2x" fixedWidth swapOpacity spin={false} mask={['far', 'circle']}/>
                <FontAwesomeIcon icon={faStreetView} color='pink' size="2x" fixedWidth swapOpacity spin={false} mask={['far', 'circle']}/>
                <h3>People in room: 3/5</h3>
                </div>
                
            </div>

            <div className={DashboardCSS['first-row']}>
                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="temp-label">Temperature: 27°C</h3>
                    <img
                        src={temp_icon}
                        width={'70%'}
                        height={'100%'}
                        alt="temp_icon"
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="humid-label">Humidity: 40%</h3>
                    <img
                        src={humid_icon}
                        width={'70%'}
                        height={'100%'}
                        alt="temp_icon"
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="moist-label">Moisture: 50%</h3>
                    
                    <img
                        src={moist_icon}
                        width={'70%'}
                        height={'100%'}
                        alt="temp_icon"
                        options={{ maintainAspectRatio: false }}
                    />
                </div>
            </div>

            <div className={`${DashboardCSS['second-row']}`}>
                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="people-label">Number of people present: 3</h3>
                    <img
                        src={human_icon}
                        width={'70%'}
                        height={'100%'}
                        alt="temp_icon"
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

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
        </div>
    );
};

export default Dashboard;
