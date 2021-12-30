import React from 'react';

import styled from 'styled-components';

const Container = styled.div`
    // width: 100%;
    height: 30px;
    padding: 20px 50px;
    background-color: #fff;
    font-family: 'SVN-Gilroy Bold';
    font-weight: bold;
    box-shadow: 5px 2px 5px 2px #ddd;
    z-index: -1;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

const locations = {
    '/': 'Dashboard',
    '/dashboard': 'Dashboard',
    '/about': 'About',
    '/live': 'Live',
    '/analytics': 'Analytics',
    '/settings': 'Settings',
};

const NavBar = (props) => {
    return (
        <Container>
            <h1>{locations[props.title]}</h1>
            <div style={{display:'flex', alignItems: 'center'}}>
                <p style={{margin: '0 10px'}}>Admin</p>
                <img
                    src="https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png"
                    alt=""
                    width="20px"
                    />
            </div>
        </Container>
    );
};

export default NavBar;
