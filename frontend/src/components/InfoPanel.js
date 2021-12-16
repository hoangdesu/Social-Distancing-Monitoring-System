import React, { useState } from 'react';

import Thermometer from './Thermometer';
import { Humidity } from 'react-environment-chart';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStreetView } from '@fortawesome/free-solid-svg-icons';
import ProgressBar from 'react-customizable-progressbar';
import moistIcon from '../assets/icons/moisture.png';

import DashboardCSS from './Dashboard.module.css';

const InfoPanel = (props) => {
    const { measurements, peopleNum } = props;

    const maxPeople = 5;
    const peopleIcons = [1, 2, 3, 4, 5];
    const [activeColor, disabledColor] = ['green', 'pink'];

    return (
        <div
            className={`${DashboardCSS['card']} ${DashboardCSS['info-panel']}`}
        >
            {/* PEOPLE IN ROOM */}
            <div className={`${DashboardCSS.sensor}`}>
                <p style={{ color: peopleNum < 5 ? '#450a1a' : '#f20000' }}>
                    {peopleNum < 5 ? 'Welcome in!' : 'Room is full!'}
                </p>
                <h2>
                    {peopleNum}/{maxPeople}
                </h2>
                <div className={`${DashboardCSS['people-icons']}`}>
                    {peopleIcons.map((i) => (
                        <FontAwesomeIcon
                            icon={faStreetView}
                            color={
                                peopleNum % (maxPeople + 1) >= `${i}`
                                    ? activeColor
                                    : disabledColor
                            }
                            size="2x"
                            fixedWidth
                        />
                    ))}
                </div>
                <h4>Number of people in room</h4>
            </div>

            {/* TEMPERATURE */}
            <div className={`${DashboardCSS.sensor}`}>
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

            {/* HUMIDITY */}
            <div className={`${DashboardCSS.sensor}`}>
                <Humidity
                    value={measurements.humidity}
                    height={100}
                    tips={['Low', 'Comfortable', 'High']}
                />
                <p className={`${DashboardCSS.humidity}`}>
                    {measurements.humidity}%
                </p>
                <h4>Humidity</h4>
            </div>

            {/* MOISTURE */}
            <div className={`${DashboardCSS.sensor} ${DashboardCSS.indicator}`}>
                <ProgressBar
                    radius={50}
                    progress={measurements.moisture}
                    cut={120}
                    rotate={-210}
                    strokeWidth={10}
                    strokeColor="#5d9cec"
                    // strokeLinecap="square"
                    trackStrokeWidth={5}
                    trackStrokeColor="#e6e6e6"
                    trackStrokeLinecap="square"
                    pointerRadius={0}
                    initialAnimation={true}
                    transition="1.5s ease 0.5s"
                    trackTransition="0s ease"
                    className={`${DashboardCSS.progressBar}`}
                >
                    <p className={`${DashboardCSS.percentage}`}>
                        {measurements.moisture}%
                    </p>
                </ProgressBar>
                <img
                    src={moistIcon}
                    alt=""
                    width="50px"
                    className={`${DashboardCSS.logo}`}
                />
                <h4>Moisture</h4>
            </div>
        </div>
    );
};

export default InfoPanel;
