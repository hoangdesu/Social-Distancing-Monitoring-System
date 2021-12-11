import React, { useState, useEffect } from 'react';
import faker from 'faker';
//import textfile from "../../../backend/habitat/message.txt"
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
} from 'chart.js';
import { Chart, Doughnut, Line } from 'react-chartjs-2';

import DashboardCSS from './Dashboard.module.css';
import axios from 'axios';
import DashElementSmall from './DashElementSmall';

{
    /* <Chart
  type={...}
  options={...}
  data={...}
  {...props}
/> */
}

// SAMPLE DATA
ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export const data = {
    // labels: ['Red', 'Blue'],
    labels: [],
    datasets: [
        {
            // label: ' # of Votes',
            data: [10, 1],
            backgroundColor: [
                'rgba(255, 206, 86, 0.2)',
                'rgba(255, 99, 132, 0.2)',
            ],
            borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
            borderWidth: 1,
        },
    ],
};

// SAMPLE DATA

export const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Total number of people going in and out',
        },
    },
};

const labels = ['In', 'Out'];

export const data1 = {
    labels,
    datasets: [
        {
            label: 'In',
            data: labels.map(() =>
                faker.datatype.number({ min: -1000, max: 1000 })
            ),
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
            label: 'Out',
            data: labels.map(() =>
                faker.datatype.number({ min: -1000, max: 1000 })
            ),
            borderColor: 'rgb(53, 162, 235)',
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
        },
    ],
};

class FancyButton extends React.Component {
    // This syntax ensures `this` is bound within handleClick.  // Warning: this is *experimental* syntax.  
    handleClick = () => {
        if (document.getElementById("qr-mask").style.display ===  "none")    
            document.getElementById("qr-mask").style.display = "block"
        else
            document.getElementById("qr-mask").style.display = "none"
    }
    render() {
      return (
        <button onClick={this.handleClick}>
          Click me
        </button>
      );
    }
  }

class MyDashBoard extends React.Component {
    measurements = {
        moisture: "",
        temperature: "",
        humidity: ""
      };

    componentDidMount() {
      document.getElementById("qr-mask").style.display =  "none";
      this.getData();
      this.interval = setInterval(() => {
        this.getData();
      }, 3000);
    }

  
    getData() {

        axios.get('http://localhost:7000/measurements/latest/')
        .then(res => {
            console.log(res.data[0])
            document.getElementById("temp-label").innerHTML = 'Temperature: ' + res.data[0].celcius + ' °C'
            document.getElementById("humid-label").innerHTML = 'Humidity: ' + res.data[0].humidity + ' %'
            document.getElementById("moist-label").innerHTML = 'Moisture: ' + res.data[0].moisture + ' %'
            if (res.data[0].created != undefined) {
                const time = res.data[0].created.split("T")
                const rm_mili = time[1].split(".")
                document.getElementById("update-time").innerHTML = 'Last Updated: ' + time[0] + ' at ' + rm_mili[0]
            }
        })

        axios.get('http://localhost:7000/entry/all')
        .then(res => {
            console.log(res.data[0])
            document.getElementById("people-label").innerHTML = 'Number of people present: ' + res.data[0].entry_number
        })

        axios.get('http://localhost:7000/message/latest')
        .then(res => {
            console.log(res.data[0])
            if (res.data[0].content == "QR Scan is done") {
                document.getElementById("qr-mask").style.display = "none"
            }
            
            else if (res.data[0].content = "QR Check!") {
                document.getElementById("qr-mask").style.display = "block"
            }
        })
    }
  
   componentWillUnmount() {
     clearInterval(this.interval);
   }
  
    render() {
      return <h3 id="update-time">Last Updated: </h3>;
    }
  }

const Dashboard = () => {
   
    return (
       
        <div className={DashboardCSS.container}>
            <FancyButton/>
            <MyDashBoard/>
            {/* <p>Dashboard</p> */}
            {/* <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} /> */}

            <div className={DashboardCSS['first-row']}>
                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="temp-label">Temperature: 27°C</h3>
                    <Doughnut
                        id="temp"
                        data={data}
                        width={'30%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="humid-label">Humidity: 40%</h3>
                    <Doughnut
                        id="humid"
                        data={data}
                        width={'50%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="moist-label">Moisture: 50%</h3>
                    <Doughnut
                        id="moist"
                        data={data}
                        width={'50%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>
            </div>

            <div className={`${DashboardCSS['second-row']}`}>
                <div 
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3 id="people-label">Number of people present: 3</h3>
                    <Doughnut
                        id="moist"
                        data={data}
                        width={'50%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>
                <div className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}>
                    <h3>Service status</h3>
                    <p>- Motion sensor: working</p>
                    <p>- PIR sensor: working</p>
                    <p>- QR reader: idle</p>
                    <p>- Stream server: connected</p>
                    <p>- Temperature sensor: stopped</p>
                </div>
                <div 
                    id = "qr-mask" className={`${DashboardCSS['card']} ${DashboardCSS['medium-element']}`}
                >
                    <div>
                        <img src="http://192.168.137.51:5000/video_feed" alt="QR_Camera" />
                    </div>
                    {/* <h3>Total people</h3>
                    <Line options={options} data={data1} /> */}
                </div>
            </div>

            {/* <img src="https://cdn.mos.cms.futurecdn.net/S5bicwPe8vbP9nt3iwAwwi.jpg" style={{ width: '80%'}}></img> */}
        </div>
    );
};

export default Dashboard;
