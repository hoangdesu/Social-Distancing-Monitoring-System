import React, { useState } from 'react';

import Thermometer from './Thermometer';
import { Humidity } from 'react-environment-chart';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faStreetView } from '@fortawesome/free-solid-svg-icons';

import DashboardCSS from './Dashboard.module.css';

const InfoPanel = (props) => {
    const { measurements, peopleNum } = props;

    const maxPeople = 5;
    const peopleIcons = [1, 2, 3, 4, 5];
    const [activeColor, disabledColor] = ['green', 'pink'];
    const [ppl, setPpl] = useState(peopleNum);
    

    // only for testing graph responsive data
    const changePpl = (option) => {
        if (option === 'add') {
            setPpl((prev) => {
                if (prev >= 0 && prev < 5) return prev + 1;
                else return prev;
            });
        } else if (option === 'remove') {
            setPpl((prev) => {
                if (prev > 0 && prev <= 5) return prev - 1;
                else return prev;
            });
        }
    };


    return (
        <div
            className={`${DashboardCSS['card']} ${DashboardCSS['info-panel']}`}
        >
            <div className={`${DashboardCSS.sensor}`}>
                <button onClick={() => changePpl('remove')}>Remove</button>
                <button onClick={() => changePpl('add')}>Add</button>
                <p>(Message)</p>
                <h2>
                    {ppl}/{maxPeople}
                </h2>
                <div className={`${DashboardCSS['people-icons']}`}>
                    {peopleIcons.map((i) => (
                        <FontAwesomeIcon
                            icon={faStreetView}
                            color={
                                ppl % (maxPeople + 1) >= `${i}`
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
            <div className={`${DashboardCSS.sensor}`}>
                <Humidity
                    value={measurements.humidity}
                    height={100}
                    tips={['10%', '60%', '100%']}
                />
                <h4>Humidity</h4>
            </div>
            <div className={`${DashboardCSS.sensor}`}>
                <p>(use progress bar)</p>
                <h4>Moisture chart</h4>
                {/* https://morioh.com/p/f593c7f8cfb0 */}
                {/* https://www.npmjs.com/package/react-sweet-progress-simdi */}
            </div>
            
        </div>
    );
};

export default InfoPanel;
