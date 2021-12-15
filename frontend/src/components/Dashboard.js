import React, { useState, useEffect } from 'react';
import faker from 'faker';
import temp_icon from './../assets/temp-icon.jpg'
import moist_icon from './../assets/moist-icon.jpg'
import humid_icon from './../assets/humid-icon.jpg'
import human_icon from './../assets/people-icon.jpg'
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
      this.getData();
      this.interval = setInterval(() => {
        this.getData();
      }, 3000);
    }

  
    getData() {
        axios.get('http://localhost:7000/measurements/latest/')
        .then(res => {
            if (parseFloat(res.data[0].celcius) !== 0) {
                console.log(res.data[0])
                document.getElementById("temp-label").innerHTML = 'Temperature: ' + res.data[0].celcius + ' °C'
                document.getElementById("humid-label").innerHTML = 'Humidity: ' + res.data[0].humidity + ' %'
                document.getElementById("moist-label").innerHTML = 'Moisture: ' + res.data[0].moisture + ' %'
                if (res.data[0].created != undefined) {
                    const time = res.data[0].created.split("T")
                    const rm_mili = time[1].split(".")
                    document.getElementById("update-time").innerHTML = 'Last Updated: ' + time[0] + ' at ' + rm_mili[0] + ' GMT: 0'
                }
            }
        })

        axios.get('http://localhost:7000/entry/all')
        .then(res => {
            console.log(res.data[0]);
 
            if (parseInt(res.data[0].entry_number) < 0) res.data[0].entry_number = "0";
            document.getElementById("people-label").innerHTML = 'Number of people present: ' + res.data[0].entry_number;
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
    const URL_video = "http://192.168.137.51:5000/video_feed"

    return (
       
        <div className={DashboardCSS.container}>
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
                <div className={`${DashboardCSS['card']} ${DashboardCSS['medium-element']}`}>
                    <h3>Members - Group 4</h3>
                    <p>s3755614,Tran Kim Long,0797999956</p>
                    <p>s3694551,Bui Minh Triet,0903162810</p>
                    <p>s3818298,Tran Minh Hoang,0819342323</p>
                    <p>s3688165,Tran Hoang Nam,0981491095</p>
                    <p>s3772163,Ta Hien Thuan,0703306422</p>
                    <p>s3697305,Nguyen Quoc Hoang,0913172602</p>
                    <p>s3740941,Lee Eunseo,0368773931</p>
                </div>
                <div 
                    id = "qr-mask" className={`${DashboardCSS['card']} ${DashboardCSS['medium-element']}`}
                >
                    <div>
                        <img src={URL_video} alt="QR_Camera" />
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
