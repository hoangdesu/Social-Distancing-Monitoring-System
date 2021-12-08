import React, { useState, useEffect } from 'react';
import faker from 'faker';

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
            // label: '# of Votes',
            data: [5, 1],
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

const Dashboard = () => {
    // const
    return (
        <div className={DashboardCSS.container}>
            {/* <p>Dashboard</p> */}
            {/* <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} />
            <DashElementSmall styling={DashboardCSS['small-element']} /> */}

            <div className={DashboardCSS['first-row']}>
                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3>Temperature: 27°C</h3>
                    <Doughnut
                        data={data}
                        width={'30%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3>Humidity: 40%</h3>
                    <Doughnut
                        data={data}
                        width={'50%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>

                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['small-element']}`}
                >
                    <h3>Moisture: 50%</h3>
                    <Doughnut
                        data={data}
                        width={'50%'}
                        height={'50%'}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>
            </div>

            <div className={`${DashboardCSS['second-row']}`}>
                <div
                    className={`${DashboardCSS['card']} ${DashboardCSS['large-element']}`}
                >
                    <h3>Total people</h3>
                    <Line options={options} data={data1} />
                </div>
                <div className={`${DashboardCSS.card} ${DashboardCSS['live-feed']}`}>
                    <h3>Service status</h3>
                    <p>- Motion sensor: working</p>
                    <p>- PIR sensor: working</p>
                    <p>- QR reader: idle</p>
                    <p>- Stream server: connected</p>
                    <p>- Temperature sensor: stopped</p>
                </div>
            </div>

            {/* <img src="https://cdn.mos.cms.futurecdn.net/S5bicwPe8vbP9nt3iwAwwi.jpg" style={{ width: '80%'}}></img> */}
        </div>
    );
};

export default Dashboard;
