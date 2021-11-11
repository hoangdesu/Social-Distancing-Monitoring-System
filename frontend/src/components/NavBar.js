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
`;

const NavBar = (props) => {
    const locations = {
        '/': 'Dashboard',
        '/dashboard': 'Dashboard',
        '/about': 'About',
        '/live': 'Live',
        '/analytics': 'Analytics',
        '/settings': 'Settings'
    }

    return (
        <Container>
            <h1>{locations[props.title]}</h1>
        </Container>
    )
}

export default NavBar;
